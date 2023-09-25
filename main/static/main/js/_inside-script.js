let list = document.querySelectorAll('.list');
let openModal = document.getElementById('open-modal')
let modalContainer = document.getElementById('modal-container')
let cancelModal = document.getElementById('cancel-modal')


let uploadFiles = [];
const types = ['audio/mpeg','audio/ogg','audio/wav']
// const types = ['image/jpeg']
let uploadList = document.querySelector('.upload-list')



for (let i=0; i<list.length; i++) {
    list[i].onclick = function(){
        let j = 0;
        while (j<list.length) {
            list[j++].classList.remove('active');
        }
        list[i].classList.add('active');
    }
}

openModal.onclick = function(){
    modalContainer.classList.add('active');
};

cancelModal.onclick = function(){
    const cleanList = document.querySelector('.upload-list');
    cleanList.innerHTML='';
    modalContainer.classList.remove('active');
    // Написать удаление всех элементов с массива файлов
}

const dragDrop = () => {
    const dragDropArea = document.querySelector('.drag-and-drop-area');
    const onDragEnter = () => dragDropArea.classList.add('drag-hover');
    const onDragLeave = () => dragDropArea.classList.remove('drag-hover');
    const prevents = (e) => e.preventDefault();

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
        dragDropArea.addEventListener(evtName, prevents);
    });

    ['dragenter', 'dragover'].forEach(evtName => {
        dragDropArea.addEventListener(evtName, onDragEnter);
    });

    ['dragleave', 'drop'].forEach(evtName => {
        dragDropArea.addEventListener(evtName, onDragLeave);
    });

    dragDropArea.addEventListener("drop", handleDrop);

}


const handleDrop = (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    for (let key in files) {
        if (!types.includes(files[key].type)) {
            continue;
        }
        uploadFiles.push(files[key]);

        let uploadURL = URL.createObjectURL(files[key])

        // uploadList.innerHTML += `<div class="upload-list-file" attribut=${uploadFiles.indexOf(files[key])}><i class="bi bi-file-earmark-music"></i><span>${files[key].name}</span><i name="del" class="bi bi-x" attribut=${uploadFiles.indexOf(files[key])} onclick="delFile(this)"></i></div>`
        uploadList.innerHTML += `<div class="upload-list-file" attribut=${uploadFiles.indexOf(files[key])} src="${uploadURL}"><i class="bi bi-file-earmark-music"></i><span>${files[key].name}</span><i name="del" class="bi bi-x" attribut=${uploadFiles.indexOf(files[key])}></i></div>`
        let els = document.getElementsByName("del");
        els.forEach(function(item) {
            item.addEventListener("click", function(){
                item.parentNode.parentNode.removeChild(item.parentNode);
                let index = this.getAttribute('attribut')
                console.log(index)
                console.log(uploadFiles)
                uploadFiles.splice(index,1);
                console.log(uploadFiles)
                // Надо написать цикл, который будет каждый раз при удалении элемента с определенным индексом, к индексам большим выбранному уменьшить на 1
            });
        });


    }
    
    
    console.log(uploadFiles)
}

document.addEventListener("DOMContentLoaded", dragDrop);



// function delFile(clicked_object) {
// 	let index = clicked_object.getAttribute('attribut')
//     console.log(index)
//     console.log(uploadFiles)
//     uploadFiles.splice(index,1);
//     console.log(uploadFiles)
//     /* alert(clicked_object.getAttribute('attribut')); */
//     let els = document.getElementsByName("del");
// 	els.forEach(function(item) {
//     item.addEventListener("click", function(){
//         item.parentNode.parentNode.removeChild(item.parentNode);
//     });
// 	});
// }



    let els = document.getElementsByName("del");
	els.forEach(function(item) {
    item.addEventListener("click", function(){
        item.parentNode.parentNode.removeChild(item.parentNode);
        let index = this.getAttribute('attribut')
        console.log(index)
        // console.log(uploadFiles)
        // uploadFiles.splice(index,1);
        // console.log(uploadFiles)
    });
	});