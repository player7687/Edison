let modalContainer = document.getElementById('modal-container');
let openModal = document.getElementById('open-modal')
let openModalMob = document.getElementById('open-modal-mob')
let cancelModal = document.getElementById('cancel-modal')
let inputElement = document.getElementById('input-file')

const list = document.querySelectorAll('.list');
function activelink(){
    list.forEach((item)=>item.classList.remove('active'));
    this.classList.add('active');
}
list.forEach((item)=> 
   item.addEventListener('click', activelink));

openModal.onclick = function(){
    modalContainer.classList.add('active');
};

cancelModal.onclick = function(){
    // const cleanList = document.querySelector('.upload-list');
    // cleanList.innerHTML='';
    
    modalContainer.classList.remove('active');
    // Написать удаление всех элементов с массива файлов
};

openModalMob.onclick = function(){
    modalContainer.classList.add('active');
};

inputElement.addEventListener("change", handleFiles, false);
function handleFiles() {
    const FileList = this.files;
    console.log(FileList);
};

let uploadFiles = [];
const types = ['audio/mpeg','audio/ogg','audio/wav']
// const types = ['image/jpeg']
let uploadList = document.querySelector('.upload-list')

inputElement.addEventListener("change", handleFiles, false);
function handleFiles() {
    const fileList = this.files; /* now you can work with the file list */
    for (let i = 0, numFiles = fileList.length; i < numFiles; i++) {
        const file = fileList[i];
        // if (!types.includes(files[key].type)) {
        //     continue;
        // }
        uploadList.innerHTML = `<div class="upload-list-file"><i class="bi bi-file-earmark-music"></i><span>${file.name}</span></div>`          
    }
}