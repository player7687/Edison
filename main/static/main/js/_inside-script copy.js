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
    modalContainer.classList.remove('active');
}

const dragDrop = () => {
    const dragDropArea = document.querySelector('.drag-and-drop-area');
    const onDragEnter = () => dragDropArea.classList.add('drag-hover');
    const onDragLeave = () => dragDropArea.classList.remove('drag-hover');
    // const onDrop = () => dragDropArea.classList.remove('drag-hover');
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
        uploadList.innerHTML += `<div class="upload-list-file"><i class="bi bi-file-earmark-music"></i><span>${files[key].name}</span><i class="bi bi-x" onclick="delFile()"></i></div>`                           
    }
    
    
    console.log(uploadList)
}

document.addEventListener("DOMContentLoaded", dragDrop);