let data = $('.card-body > p')
for (item of data) {
    if (!item.innerHTML) {
       item.innerHTML = 'Товар с баркодом'
       item.style.color = 'red'
    }
}