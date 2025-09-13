document.querySelector('#switch-file-choose').addEventListener('change', function() {
    document.querySelector('#switch-file-choose-form').submit();
})

function setDataType(inputId, typeId) {
  const input = document.getElementById(inputId);
  const type = document.getElementById(typeId).value;

  input.value = ""
  switch (type) {
    case "2":
      input.type = 'text';
      break;
    case "3":
      input.type = 'number';
      input.step = '1';
      break;
    case "4":
      input.type = 'number';
      input.step = 'any';
      break;
    case "5":
      input.type = 'time';
      break;
    case "6":
      input.type = 'date';
      break;
    case "7":
      input.type = 'datetime-local';
      break;
    default:
      input.type = 'text';
  }
}