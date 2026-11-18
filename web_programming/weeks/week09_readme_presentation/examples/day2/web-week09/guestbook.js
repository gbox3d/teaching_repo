const form = document.querySelector('#guestbook-form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
const dateFormat = new Intl.DateTimeFormat('ko-KR', { dateStyle: 'medium', timeStyle: 'short' });

function clearNotice() {
  notice.textContent = '';
}

function createPost(name, message, createdAt) {
  const li = document.createElement('li');
  const post = document.createElement('article');
  post.className = 'post';

  const avatar = document.createElement('span');
  avatar.className = 'post-avatar';
  avatar.setAttribute('aria-hidden', 'true');
  avatar.textContent = Array.from(name)[0];

  const content = document.createElement('div');
  content.className = 'post-content';
  const meta = document.createElement('div');
  meta.className = 'post-meta';
  const author = document.createElement('h3');
  author.className = 'post-author';
  author.textContent = name;
  const time = document.createElement('time');
  time.dateTime = createdAt.toISOString();
  time.textContent = dateFormat.format(createdAt);

  const body = document.createElement('p');
  body.className = 'post-body';
  body.textContent = message;
  meta.append(author, time);
  content.append(meta, body);
  post.append(avatar, content);
  li.append(post);
  return li;
}

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const name = nameInput.value.trim();
  const message = messageInput.value.trim();

  if (name === '') {
    notice.textContent = '이름을 입력하세요.';
    nameInput.focus();
    return;
  }

  if (message === '') {
    notice.textContent = '메시지를 입력하세요.';
    messageInput.focus();
    return;
  }

  clearNotice();
  const li = createPost(name, message, new Date());
  list.prepend(li);
  form.reset();
  nameInput.focus();
});

nameInput.addEventListener('input', clearNotice);
messageInput.addEventListener('input', clearNotice);
