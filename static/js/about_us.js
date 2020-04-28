function load_people() {

var person = [
    {
        name:"Никита Гудков",
        role:"Teamleader, Fullstack, Project guru",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Андрей Ткачёв",
        role:"Teamleader, Fullstack, Git, Project guru",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Андрей Мухин",
        role:"Backend",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Анна Буше",
        role:"Backend",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Владислав Харченко",
        role:"Backend",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
    {
        name:"Евгений Маринин",
        role:"Frontend",
        email:"wow@mail.huh",
        twitter:"#",
        facebook:"#",
        instagram:"#",
        photo_file:"profile_icon.png",
    },
];
var people_HTML = '';

for (i = 0; i < 6; i++) {
    var photo_HTML = '<div class="img-block">\n' +
                     '    <img src="\/static\/img\/profile\/' + person[i].photo_file + '">\n' +
                     '</div>\n';
    var contacts_block_HTML = '<div class="contacts-block">\n' +
                              '    <h3>' + person[i].name + '</h3>\n' +
                              '    <p>' + person[i].role + '</p>\n' +
                              '    <a href="mailto:' + person[i].email + '">' + person[i].email + '</a>\n' +
                              '    <ul class="icons">\n' +
                              '        <li><a href="' + person[i].facebook +'" class="icon brands fa-facebook-f"><span class="label">Facebook</span></a></li>\n' +
                              '        <li><a href="' + person[i].twitter +'" class="icon brands fa-twitter"><span class="label">Twitter</span></a></li>\n' +
                              '        <li><a href="' + person[i].instagram +'" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>\n' +
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