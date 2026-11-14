function buildRequest(method, book, id, bodyText, editKey) {
  if (!/^[a-z0-9_-]{1,40}$/.test(book)) throw new Error('방명록 번호를 확인하세요.');
  if (id !== '' && !/^[1-9][0-9]*$/.test(id)) throw new Error('글 ID는 양의 정수로 입력하세요.');
  if (method === 'PATCH' || method === 'DELETE') {
    if (id === '') throw new Error('수정·삭제할 글 ID를 입력하세요.');
  }
  const url = new URL('/rest/v1/guestbook', API_BASE_URL);
  const options = { method: method, headers: { apikey: API_PUBLIC_KEY } };
  if (method !== 'POST') {
    url.searchParams.set('book_id', `eq.${book}`);
    if (id !== '') url.searchParams.set('id', `eq.${id}`);
    if (method === 'GET') {
      url.searchParams.set('order', 'id.desc');
      url.searchParams.set('limit', '50');
    }
  }
  if (method === 'PATCH' || method === 'DELETE') options.headers['X-Edit-Key'] = editKey;
  if (method === 'POST' || method === 'PATCH') {
    const body = JSON.parse(bodyText);
    if (body === null || Array.isArray(body) || typeof body !== 'object') {
      throw new Error('JSON 객체 하나를 입력하세요.');
    }
    options.headers['Content-Type'] = 'application/json';
    options.headers.Prefer = 'return=representation';
    options.body = JSON.stringify(body);
  }
  return { url: url.href, options: options };
}
