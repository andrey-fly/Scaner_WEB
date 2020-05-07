function load_people() {

var person = [
    {
        name:"Никита Гудков",
        role:"Teamleader, Fullstack, Project guru",
        email:"nikitaster2001@gmail.com",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Андрей Ткачёв",
        role:"Teamleader, Fullstack, Git, Project guru",
        email:"sim200347@gmail.com",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Андрей Мухин",
        role:"Backend",
        email:"muhinav14@mail.ru",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Анна Буше",
        role:"Backend",
        email:"annbushe@yandex.ru",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Владислав Харченко",
        role:"Backend",
        email:"vladislavharcenko14@gmail.com",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Евгений Маринин",
        role:"Frontend",
        email:"marinin2003@yandex.ru",
        vk:"#",
        twitter:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
];
var people_HTML = '';

for (i = 0; i < 6; i++) {
    var photo_HTML = '<div class="img-block" style="max-width: 100px; height: auto">\n' +
                     '    <img src="\/static\/img\/profile\/' + person[i].photo_file + '">\n' +
                     '</div>\n';
    var contacts_block_HTML = '<div class="contacts-block">\n' +
                              '    <h3>' + person[i].name + '</h3>\n' +
                              '    <p>' + person[i].role + '</p>\n' +
                              '    <a href="mailto:' + person[i].email + '">' + person[i].email + '</a>\n' +
                              '    <ul class="icons">\n' +
                              '        <li><a href="' + person[i].facebook +'" class="icon brands fa-vk"><span class="label">Facebook</span></a></li>\n' +
                              '        <li><a href="' + person[i].twitter +'" class="icon brands fa-twitter"><span class="label">Twitter</span></a></li>\n' +
                              '        <li><a href="' + person[i].instagram +'" class="icon brands fa-telegram-plane"><span class="label">Instagram</span></a></li>\n' +
                              '    </ul>\n' +
                              '</div>\n';
    if (i % 2 == 0) {
        people_HTML += '    <div class="people-group">\n' + photo_HTML + contacts_block_HTML;
    } else {
        people_HTML += contacts_block_HTML + photo_HTML + '    </div>\n';
    }
}
document.getElementById("participants-info-block").innerHTML = people_HTML;

}

window.onload = load_people();
