// AIV Designs enquiry form: receives the website form and emails it to the studio inbox.
// Runs on Cloudflare Workers at aivdesigns.co.uk/api/enquiry. The send_email binding
// (MAIL) can only deliver to the verified address in its binding, so it cannot be used
// to send mail anywhere else.
import { EmailMessage } from 'cloudflare:email';

const ALLOWED = /^https:\/\/(www\.)?aivdesigns\.co\.uk$/;
const FROM = 'enquiries@aivdesigns.co.uk';

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

// one line, no control characters, capped
const line = (v, n) => String(v ?? '').replace(/[\u0000-\u001f\u007f]+/g, ' ').trim().slice(0, n);
// free text keeps its line breaks
const text = (v, n) => String(v ?? '').replace(/\r\n?/g, '\n').replace(/[\u0000-\u0008\u000b-\u001f\u007f]/g, '').trim().slice(0, n);

const b64 = (s) => {
  const bytes = new TextEncoder().encode(s);
  let bin = '';
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
};
const wrap = (s) => s.replace(/(.{76})/g, '$1\r\n');
const header = (s) => (/^[\x20-\x7e]*$/.test(s) ? s : '=?UTF-8?B?' + b64(s) + '?=');

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204 });
    if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405);

    const origin = request.headers.get('Origin') || '';
    if (origin && !ALLOWED.test(origin)) return json({ ok: false, error: 'origin' }, 403);

    const len = Number(request.headers.get('content-length') || 0);
    if (len > 20000) return json({ ok: false, error: 'size' }, 413);

    let d;
    try { d = await request.json(); } catch { return json({ ok: false, error: 'format' }, 400); }

    // spam traps: a field people never see, and a form filled faster than a person can
    if (line(d.website, 200)) return json({ ok: true });
    const took = Number(d.took || 0);
    if (!(took >= 3000)) return json({ ok: true });

    const name = line(d.name, 120);
    const business = line(d.business, 160);
    const contact = line(d.contact, 200);
    const type = line(d.type, 80) || 'Not given';
    const message = text(d.message, 4000);
    if (!name || !business || !contact) return json({ ok: false, error: 'missing' }, 422);

    const replyTo = /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(contact) ? contact : '';
    const body =
      'New enquiry from aivdesigns.co.uk\n\n' +
      'Name: ' + name + '\n' +
      'Business: ' + business + '\n' +
      'Email or phone: ' + contact + '\n' +
      'Type of business: ' + type + '\n' +
      (message ? '\nWhat the site should do:\n' + message + '\n' : '') +
      '\nSent ' + new Date().toUTCString() + '\n';

    const id = crypto.randomUUID();
    const raw = [
      'From: ' + header('AIV Designs website') + ' <' + FROM + '>',
      'To: <' + env.DEST + '>',
      replyTo ? 'Reply-To: <' + replyTo + '>' : null,
      'Subject: ' + header('New enquiry: ' + business),
      'Date: ' + new Date().toUTCString(),
      'Message-ID: <' + id + '@aivdesigns.co.uk>',
      'MIME-Version: 1.0',
      'Content-Type: text/plain; charset=utf-8',
      'Content-Transfer-Encoding: base64',
      '',
      wrap(b64(body)),
    ].filter((x) => x !== null).join('\r\n');

    try {
      await env.MAIL.send(new EmailMessage(FROM, env.DEST, raw));
    } catch (e) {
      console.error('send failed', e && e.message);
      return json({ ok: false, error: 'send' }, 502);
    }
    return json({ ok: true });
  },
};
