const showPostButton = document.querySelector('#show-post');
const newPost = document.querySelector('#new-post');

showPostButton.addEventListener('click', function () {
  newPost.hidden = false;
  showPostButton.hidden = true;
  newPost.querySelector('h2').focus();
});
