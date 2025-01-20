var myImage = document.querySelector('img');

myImage.onclick = function() {
    var mySrc = myImage.getAttribute('src');
    if(mySrc === 'image/me.jpg') {
      myImage.setAttribute ('src','image/me-2.jpg');
    } else {
      myImage.setAttribute ('src','image/me.jpg');
    }
}