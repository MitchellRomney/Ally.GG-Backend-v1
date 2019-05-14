function errorHandling() {
    let errorVm = new Vue({
        delimiters: ['[[', ']]'],
        el: '#errors',
        data: {
            isError: false,
            errorMessage: '',
        }
    });
}