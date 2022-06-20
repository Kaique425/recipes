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