const client = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const list = document.querySelector('#list');
const notice = document.querySelector('#notice');

async function showList() {
  const result = await client
    .from('guestbook')
    .select('name, message, created_at')
    .order('created_at', { ascending: false });

  if (result.error) {
    notice.textContent = '불러오지 못했습니다: ' + result.error.message;
    return;
  }

  const items = result.data;
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const date = new Date(items[i].created_at).toLocaleDateString();
    const li = document.createElement('li');
    li.textContent = `${items[i].name}: ${items[i].message} (${date})`;
    list.append(li);
  }
  notice.textContent = `방명록 ${items.length}개`;
}

form.addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '' || message === '') {
    notice.textContent = '이름과 메시지를 모두 입력하세요.';
    return;
  }

  const result = await client
    .from('guestbook')
    .insert({ name: name, message: message });

  if (result.error) {
    notice.textContent = '저장하지 못했습니다: ' + result.error.message;
    return;
  }

  form.reset();
  nameInput.focus();
  showList();
});

showList();
