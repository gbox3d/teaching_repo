const list = document.querySelector('#list');
const reload = document.querySelector('#reload');
const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const bookUrl = API_BASE_URL + '/rest/v1/guestbook?book_id=eq.' + encodeURIComponent(BOOK_ID);
let deleting = false;

async function readRows(url) {
  const response = await fetch(url, { headers: { apikey: API_PUBLIC_KEY }, cache: 'no-store' });
  if (!response.ok) throw new Error('HTTP ' + response.status);
  return response.json();
}

async function loadRows() {
  reload.disabled = true;
  try {
    const rows = await readRows(bookUrl + '&select=id,name,message&order=id.desc');
    list.replaceChildren();
    for (const row of rows) {
      const item = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'w3-button w3-small w3-border w3-margin-left';
      button.textContent = '삭제';
      button.addEventListener('click', function () { deleteRow(row.id); });
      item.append('#' + row.id + ' ' + row.name + ' · ' + row.message, button);
      list.append(item);
    }
    if (!rows.length) notice.textContent = '등록된 글 없음';
  } catch (error) {
    notice.textContent = '목록 조회 실패 · ' + error.message;
  } finally {
    reload.disabled = false;
  }
}

async function deleteRow(id) {
  if (deleting || !confirm('글 ' + id + '번을 삭제하시겠습니까?')) return;
  deleting = true;
  reload.disabled = true;
  result.textContent = '';
  try {
    // 학생 수정 1: 목록에서 선택한 글 번호를 태그 조건에 추가한다.
    const url = bookUrl + '&id=eq.' + id;
    const response = await fetch(url, {
      // 학생 수정 2: 삭제 메서드를 지정한다.
      method: 'DELETE',
      // 학생 수정 3: 공용 API 키를 전송한다.
      headers: { apikey: API_PUBLIC_KEY }
    });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const remaining = await readRows(url);
    result.textContent = JSON.stringify(remaining);
    if (remaining.length) throw new Error('글이 남아 있습니다.');
    notice.textContent = '글 ' + id + '번 삭제 확인';
    await loadRows();
  } catch (error) {
    notice.textContent = '삭제 확인 실패 · ' + error.message;
  } finally {
    reload.disabled = false;
    deleting = false;
  }
}

reload.addEventListener('click', loadRows);
loadRows();
