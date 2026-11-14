editForm.addEventListener('submit', async function (event) {
  event.preventDefault();
  const id = editId.value;
  const message = editMessage.value.trim();
  if (editKey === '' || id === '' || message === '') {
    editNotice.textContent = '편집 키, 수정할 글, 메시지를 확인하세요.';
    return;
  }
  const button = document.querySelector('#save-edit');
  button.disabled = true;
  editNotice.textContent = '수정 중';
  try {
    const response = await fetch(messageUrl(id), {
      method: 'PATCH',
      headers: {
        apikey: API_PUBLIC_KEY, 'X-Edit-Key': editKey,
        'Content-Type': 'application/json', Prefer: 'return=representation'
      },
      body: JSON.stringify({ message: message })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const changed = await response.json();
    if (changed.length !== 1) throw new Error('편집 키와 글 번호를 확인하세요.');
    const saved = await readMessage(id);
    if (saved.length !== 1 || saved[0].message !== message) {
      throw new Error('저장한 글을 다시 확인하지 못했습니다.');
    }
    const loaded = await loadMessages();
    editNotice.textContent = loaded ? '수정 완료' : '수정 완료. 목록을 다시 불러오세요.';
    editForm.reset();
  } catch (error) {
    editNotice.textContent = `수정 확인 실패: ${error.message}`;
  } finally {
    button.disabled = false;
  }
});
