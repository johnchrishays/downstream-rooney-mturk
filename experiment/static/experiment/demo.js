let true_demo = JSON.parse(document.getElementById('true_demo').textContent)
let perc_demo = JSON.parse(document.getElementById('perc_demo').textContent)
let n_demo = JSON.parse(document.getElementById('n_demo').textContent)
let pts_per_dollar = JSON.parse(document.getElementById('pts_per_dollar').textContent)
let selected_demo = new Array(n_demo).fill(false)
let n_selected_demo = 0
let perc_total_demo = 0
let true_total_demo = 0
let k_demo = 3

function demo_select(i) {
  if (selected_demo[i]) {
    selected_demo[i] = !selected_demo[i];
    n_selected_demo--;
    perc_total_demo -= parseInt(perc_demo[i])
    true_total_demo -= parseInt(true_demo[i])
    el = document.getElementById(`btn_demo${i}`)
    el.classList.remove("lighten-3", "grey-text", "text-darken-3")
    el.classList.add("darken-3", "white-text")
    el.innerHTML = `${perc_demo[i]}`
    if (n_selected_demo < k_demo) {
      el = parent.document.getElementById("next_btn")
      el.classList.add("disabled")
    }
    el = document.getElementById("true_total_demo")
    el.innerHTML =  `${true_total_demo}`
    el = document.getElementById("perc_total_demo")
    el.innerHTML = `${perc_total_demo}`
    el = document.getElementById("bonus_total_demo")
    el.innerHTML = `\$${(true_total_demo/pts_per_dollar).toFixed(2)}`
  }
  else if (n_selected_demo < k_demo) {
    selected_demo[i] = !selected_demo[i];
    n_selected_demo++;
    perc_total_demo += parseInt(perc_demo[i])
    true_total_demo += parseInt(true_demo[i])
    el = document.getElementById(`btn_demo${i}`)
    el.classList.remove("darken-3", "white-text" )
    el.classList.add("lighten-3", "grey-text", "text-darken-3")
    el.innerHTML = `<del>${ perc_demo[i] }</del><br>${ true_demo[i] }`
    if (n_selected_demo == k_demo && selected_demo[0] && selected_demo[1] && selected_demo[3]) {
      el = parent.document.getElementById("next_btn")
      el.classList.remove("disabled")
    }
    el = document.getElementById("true_total_demo")
    el.innerHTML =  `${true_total_demo}`
    el = document.getElementById("perc_total_demo")
    el.innerHTML = `${perc_total_demo}`
    el = document.getElementById("bonus_total_demo")
    el.innerHTML = `\$${(true_total_demo/pts_per_dollar).toFixed(2)}`
  }
}