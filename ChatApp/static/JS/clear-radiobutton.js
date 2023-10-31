const radioButtons = document.querySelectorAll('input[type="radio"]');

const clearRadioButton = (radioButton) => {
  setTimeout(func =()=>{
    radioButton.checked = false;
  },100)
}

radioButtons.forEach(radioButton => {
  let queryStr = 'label[for="' + radioButton.id + '"]'
  let label = document.querySelector(queryStr)

  radioButton.addEventListener("mouseup", func=()=>{
    if(radioButton.checked){
      clearRadioButton(radioButton)
    }
  });

  if(label){
    label.addEventListener("mouseup", func=()=>{
      if(radioButton.checked){
        clearRadioButton(radioButton)
      }
    });
  }

});
