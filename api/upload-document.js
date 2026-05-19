import { put } from '@vercel/blob';

export const config = {
  maxDuration: 60,
};

export default async function handler(request) {
  if (request.method !== 'POST') {
    return Response.json({ error: 'Method not allowed' }, { status: 405 });
  }

  if (!process.env.BLOB_READ_WRITE_TOKEN) {
    return Response.json(
      { error: 'Document storage is not configured. Please email info@northvalepm.com.' },
      { status: 503 }
    );
  }

  try {
    const formData = await request.formData();
    const file = formData.get('file');
    if (!file || typeof file === 'string') {
      return Response.json({ error: 'No file provided' }, { status: 400 });
    }

    const maxBytes = 4 * 1024 * 1024;
    if (file.size > maxBytes) {
      return Response.json({ error: 'File exceeds the 4 MB limit' }, { status: 413 });
    }

    const safeName = (file.name || 'document').replace(/[^\w.\-]+/g, '_');
    const blob = await put('tenant-applications/' + Date.now() + '-' + safeName, file, {
      access: 'public',
      addRandomSuffix: true,
    });

    return Response.json({ ok: true, url: blob.url, filename: file.name });
  } catch (err) {
    console.error('upload-document error:', err);
    return Response.json({ error: 'Upload failed' }, { status: 500 });
  }
}
