const confirmDelete = () => {
    const form = document.querySelector("form#form-delete");
    if(form){
        form.addEventListener("submit", (event) => {
            event.preventDefault()
            const confirmed = confirm("Are you sure ?")
            if(confirmed){
                form.submit();
            };
        });
    };
};
confirmDelete();


const buttonCloseMenu = document.querySelector(".button-close-menu");
const buttonShowMenu = document.querySelector(".button-show-menu")
const menuContainer = document.querySelector(".menu-container")

const buttonShowMenuClass = "button-show-menu-visible"
const menuHiddenClass = "menu-hidden"

const closeMenu = () => {
    console.log("closeMenu")
    buttonShowMenu.classList.add(buttonShowMenuClass)   
    menuContainer.classList.add(menuHiddenClass)
}

const openMenu = () => {
    menuContainer.style.width = "261px"
    console.log("openMenu")
    buttonShowMenu.classList.remove(buttonShowMenuClass)
    menuContainer.classList.remove(menuHiddenClass)
}


const logoutForm = document.querySelector(".form-logout")
const logoutBtn = document.querySelectorAll(".logout-btn")

for (const btn of logoutBtn){
    btn.addEventListener("click", () => {
       logoutForm.submit()
    })
}
