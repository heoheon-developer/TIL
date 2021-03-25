// Write Javascript code here!


const items = document.querySelectorAll('.item');

items.forEach(function(item){
    item.addEventListener('click', function(e){
        item.classList.toggle('open');
        items.forEach(function(elem){
            if (elem !== item) elem.classList.remove('open');
        });
    });
});