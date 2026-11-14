const notice = document.querySelector('#notice');
const list = document.querySelector('#list');
function showList(items) {
  list.innerHTML = '';
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = `${items[i].id} | ${items[i].name}: ${items[i].message}`;
    list.append(li);
  }
}
