async function deleteMessage(id, button) {
  if (editKey === '') {
    editNotice.textContent = '편집 키를 먼저 입력하세요.';
    return;
  }
  if (!confirm(`글 ${id}번을 삭제하시겠습니까?`)) return;
  button.disabled = true;
  editNotice.textContent = '삭제 중';
  try {
    const response = await fetch(messageUrl(id), {
      method: 'DELETE',
      headers: { apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey }
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    // 204 응답에는 본문이 없으므로 response.json()을 호출하지 않는다.
    const remaining = await readMessage(id);
    if (remaining.length !== 0) throw new Error('편집 키와 글 번호를 확인하세요.');
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '삭제 완료' : '삭제 완료. 목록을 다시 불러오세요.';
  } catch (error) {
    editNotice.textContent = `삭제 확인 실패: ${error.message}`;
  } finally {
    button.disabled = false;
  }
}
