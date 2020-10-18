// State variables
let selected = new Array(n_x + n_y).fill(false)
let selected_counter = 0
let y_selected_counter = 0
let num_selected_x_cands = 0
let cumulative_bonus = 0
let cumulative_points = 0

let disable_select = false

$(document).ready(function(){
  $('.sidenav').sidenav();
  $('.modal').modal({dismissible: false, onOpenStart: function() { demo(-1); }});
  if (is_restore != "True") {
    $('.sidenav').sidenav('open');
    $('.modal').modal('open');
    const el = document.getElementById("startTime");
    const date = new Date();
    el.value = date.getTime();
  }
  else {
    n_iterations_remaining = n_iterations - selected_restore.length
    const frm = document.getElementById("form")
    for (i = 0; i < selected_restore.length; i++) {
      const db_entry_id_el = document.createElement("input")
      db_entry_id_el.type = "hidden"
      db_entry_id_el.name = `db_entry_id[${i+1}]`
      db_entry_id_el.value = db_entry_id_restore[i]
      frm.appendChild(db_entry_id_el)

      const round_completion_time_el = document.createElement("input")
      round_completion_time_el.type = "hidden"
      round_completion_time_el.name = `round_completion_time[${i+1}]`
      round_completion_time_el.value = round_completion_time_restore[i]
      frm.appendChild(round_completion_time_el)

      const selected_el = document.createElement("input")
      selected_el.type = "hidden"
      selected_el.name = `selected[${i+1}]`
      selected_el.value = JSON.stringify(selected_restore[i])
      frm.appendChild(selected_el)

      cumulative_points += true_utility_restore[i]
      cumulative_bonus += true_utility_restore[i] / pts_per_dollar

      Plot.data.push({"index": i+1, "score": true_utility_restore[i]})
    }
    update_plot()

    elt = document.getElementById("n_iterations_remaining")
    if (n_iterations_remaining >= 0) {
      elt.innerHTML = `Remaining rounds: ${ n_iterations_remaining }`
    }
    else {
      elt.innerHTML = `Remaining rounds: 0`
      btn = document.getElementById("btn_submit")
      btn.innerHTML = 'FINISH';
      btn.classList.remove('disabled')
      btn.onclick = render_questionnaire

      const end_time_el = document.getElementById("endTime")
      const d = new Date()
      const end_time = d.getTime()
      end_time_el.value = end_time
    }

    elt = document.getElementById("outcomes_game_num")
    elt.innerHTML = `Round #${ n_iterations - n_iterations_remaining + 1 }`

    elt = document.getElementById("cumulative_points")
    elt.innerHTML = `Cumulative points: ${ cumulative_points }`

    elt = document.getElementById("cumulative_bonus")
    elt.innerHTML = `Cumulative bonus: \$${cumulative_bonus.toFixed(2)}`
  }
});

function select(i) {
  if (disable_select) { 
    return; 
  }

  const el = document.getElementById(`${i}`);
  if (is_x[i] && (selected[i] || selected_counter < k)) {
    selected[i] = ! selected[i]
    selected_counter += selected[i] ? 1 : -1
    num_selected_x_cands += selected[i] ? 1 : -1
    if (el.className.search("darken-4") != -1) {
      el.className = "btn-block blue lighten-3 grey-text text-darken-3 btn-flat"
    }
    else {
      el.className = "btn-block blue darken-4 white-text btn-flat"
    }
  }
  else if (selected[i] || (selected_counter < k && y_selected_counter < k-l)) {
    selected[i] = ! selected[i]
    selected_counter += selected[i] ? 1 : -1
    y_selected_counter += selected[i] ? 1 : -1
    if (el.className.search("deep-orange darken-3") != -1) {
      el.className = "btn-block deep-orange lighten-3 grey-text text-darken-3 btn-flat"
    }
    else {
      el.className = "btn-block deep-orange darken-3 btn-flat white-text"
    }
  }
  const btn = document.getElementById("btn_submit");
  if (selected_counter >= k && assignment_id != "ASSIGNMENT_ID_NOT_AVAILABLE") {
    btn.onclick = submit 
    btn.classList.remove('disabled')
  } else {
    btn.onclick = "" 
    btn.classList.add('disabled')
  }
} 

function update_cands(data) {
  selected = new Array(n_x + n_y).fill(false)
  selected_counter = 0
  y_selected_counter = 0
  num_selected_x_cands = 0
  cand_strs = JSON.parse(data['cand_strs'])
  is_x = JSON.parse(data['is_x'])
  db_entry_id = JSON.parse(data['db_entry_id'])
  for (i = 0; i < n_x + n_y; i++) {
    let el = document.getElementById(i);
    el.innerHTML = cand_strs[i]
    if (is_x[i]) {
      el.className = "btn-block blue darken-4 white-text btn-flat"
    } else {
      el.className = "btn-block deep-orange darken-3 btn-flat white-text"
    }
  }

  const iters = document.getElementById("n_iterations_remaining");
  n_iterations_remaining -= 1
  iters.innerHTML = `Remaining rounds: ${n_iterations_remaining}`

  let outcomes = document.getElementById('outcomes_estimated')
  outcomes.innerHTML = "Estimated points: "
  outcomes = document.getElementById('outcomes_actual')
  outcomes.innerHTML = "True points: "

  const outcomes_game_num = document.getElementById('outcomes_game_num')
  outcomes_game_num.innerHTML = `Round #${n_iterations+1-n_iterations_remaining}`

}

function new_iteration() {
  disable_select = false
  const btn = document.getElementById("btn_submit");
  btn.onclick = ""
  btn.innerHTML = '<i class="material-icons">arrow_forward</i>'
  btn.classList.add("disabled")
  const scroll = document.getElementById("candidate_buttons")
  scroll.scrollTop = 0
  $.ajax({
    url:`/experiment/iteration/new`,
    type:"GET",
    data: {"n_x": n_x, "n_y": n_y, "k": k, "l": l, "n_iterations": n_iterations, "bias": bias},
    success: update_cands,
    error: function(data) {
      console.log("Ajax request failed.")
      console.log(data)
    }
  })
}

function demo(page) {
  el = document.getElementById("modal-body")
  iframe = document.getElementById("iframe")
  if (! iframe) {
    iframe = document.createElement("iframe")
    iframe.style = "width:100%;"
    iframe.id = "iframe"
    el.appendChild(iframe)
  }
  iframe.src = `demo/?page=${page}&pts_per_dollar=${pts_per_dollar}&k=${k}&l=${l}&n_iterations=${n_iterations}`
  next = document.getElementById("next_btn")
  if (page == -1) {
    next.onclick = function () { demo(0); }
    next.innerHTML = "NEXT"
    back = document.getElementById("back_btn")
    if (back) {
      back.remove();
    }
    next.classList.remove("disabled")
  }
  if (page == 0) {
    iframe.onload = null
    next.onclick = function () { $('.modal').modal('close'); }
    next.classList.add("disabled")
    next.innerHTML = "DONE"
    back = document.getElementById("back_btn")
    if (!back) {
      back = document.createElement("button")
      back.type = "button"
      back.id = "back_btn"
      back.innerHTML = "BACK"
      back.style = "float: right; clear: none;"
    }
    back.className="waves-effect waves-green btn-flat"
    back.onclick = function () { demo(-1); }
    el = document.getElementById("modal-content")
    el.insertBefore(back, el.childNodes[2])
  }
  $('#iframe').load(function () {
    $(this).height($(this).contents().height());
    $(this).width($(this).contents().width());
  });
}

function exit_early() {
  if (assignment_id == "ASSIGNMENT_ID_NOT_AVAILABLE") { return; }
  const frm = document.getElementById("form")
  const n_iterations_remaining_el = document.createElement("input")
  n_iterations_remaining_el.type = "hidden"
  n_iterations_remaining_el.id = `n_iterations_remaining_${n_iterations_remaining}`
  n_iterations_remaining_el.name = "n_iterations_remaining"
  n_iterations_remaining_el.value = n_iterations_remaining
  frm.appendChild(n_iterations_remaining_el)

  const end_time_el = document.getElementById("endTime")
  const d = new Date()
  const end_time = d.getTime()
  end_time_el.value = end_time

  frm.submit()
}

function render_questionnaire() {
  candidate_buttons_el = document.getElementById("candidate_buttons")
  parent_el = candidate_buttons_el.parentNode
  parent_el.removeChild(candidate_buttons_el)

  row_el = document.createElement("div")
  row_el.className = "row"
  parent_el.appendChild(row_el)

  child_el = document.createElement("div")
  child_el.className = "input-field"
  row_el.appendChild(child_el)

  const difference_red_blue_el = document.createElement("textarea")
  difference_red_blue_el.className = "materialize-textarea"
  difference_red_blue_el.form = "form"
  difference_red_blue_el.name = "difference_red_blue"
  difference_red_blue_el.id = "difference_red_blue"
  child_el.appendChild(difference_red_blue_el)

  const difference_red_blue_el_label = document.createElement("label")
  difference_red_blue_el_label.for = 'difference_red_blue'
  difference_red_blue_el_label.innerHTML = "Did you notice a difference between the red and blue buttons? If yes, what was it?"
  child_el.appendChild(difference_red_blue_el_label)

  row_el = document.createElement("div")
  row_el.className = "row"
  parent_el.appendChild(row_el)

  child_el = document.createElement("div")
  child_el.className = "input-field"
  row_el.appendChild(child_el)

  const strategy_el = document.createElement("textarea")
  strategy_el.className = "materialize-textarea"
  strategy_el.form = "form"
  strategy_el.name = "strategy"
  strategy_el.id = "strategy"
  child_el.appendChild(strategy_el)

  const strategy_el_label = document.createElement("label")
  strategy_el_label.for = 'strategy'
  strategy_el_label.innerHTML = "Did you change your strategy between the beginning and the end? If yes, how?"
  child_el.appendChild(strategy_el_label)

  row_el = document.createElement("div")
  row_el.className = "row"
  parent_el.appendChild(row_el)

  child_el = document.createElement("div")
  child_el.className = "input-field"
  row_el.appendChild(child_el)

  const reload_el = document.createElement("textarea")
  reload_el.className = "materialize-textarea"
  reload_el.form = "form"
  reload_el.name = "reload"
  reload_el.id = "reload"
  child_el.appendChild(reload_el)

  const reload_el_label = document.createElement("label")
  reload_el_label.for = 'reload'
  reload_el_label.innerHTML = "At any point did you reload the page and start over? If yes, why?"
  child_el.appendChild(reload_el_label)

  row_el = document.createElement("div")
  row_el.className = "row"
  parent_el.appendChild(row_el)

  child_el = document.createElement("div")
  child_el.className = "input-field"
  row_el.appendChild(child_el)

  const other_el = document.createElement("textarea")
  other_el.className = "materialize-textarea"
  other_el.form = "form"
  other_el.name = "other"
  other_el.id = "other"
  child_el.appendChild(other_el)

  const other_el_label = document.createElement("label")
  other_el_label.for = 'other'
  other_el_label.innerHTML = "Any other general comments or suggestions?"
  child_el.appendChild(other_el_label)

  let btn = document.getElementById("btn_submit")

  setTimeout(function() {
  // Handler for .load() called.
    btn.onclick = null
    btn.type = 'submit'
    btn.innerHTML = '<p style="line-height:100%;">SUBMIT HIT</p>';
  }, 10);
}

function update_view(data) {
  let perceived_utility = 0
  let true_utility = 0
  true_utils = JSON.parse(data["true"])
  perc_utils = JSON.parse(data["perc"])
  for (i = 0, j = 0; i < n_x + n_y; i++) {
    el = document.getElementById(i)
    if (selected[i]) {
      div = document.getElementById("btn"+i);
      el.innerHTML = `<strike>${perc_utils[j]}</strike> ${true_utils[j]}`;
      perceived_utility += parseFloat(perc_utils[j]);
      true_utility += parseFloat(true_utils[j]);
      j++;
    }
  }

  Plot.data.push({"index":n_iterations+1-n_iterations_remaining, "score":true_utility})
  update_plot()

  cumulative_points += true_utility
  cumulative_bonus += true_utility / pts_per_dollar

  let btn = document.getElementById("btn_submit")
  let frm = document.getElementById('form');

  if (n_iterations_remaining < 1) {
    if (assignment_id == "heroku") {
      frm.action = 'herokuSubmit'
      frm.method = 'GET'
    }
    btn.innerHTML = 'FINISH';
    btn.onclick = render_questionnaire

    const end_time_el = document.getElementById("endTime")
    const d = new Date()
    const end_time = d.getTime()
    end_time_el.value = end_time
  }
  else {
    btn.innerHTML = '<p style="line-height:100%;">NEXT ROUND</p>'

    btn.onclick = new_iteration
  }

  const db_entry_id_el = document.createElement("input")
  db_entry_id_el.type = "hidden"
  db_entry_id_el.name = `db_entry_id[${n_iterations+1-n_iterations_remaining}]`
  db_entry_id_el.value = db_entry_id
  frm.appendChild(db_entry_id_el)

  const round_completion_time_el = document.createElement("input")
  round_completion_time_el.type = "hidden"
  round_completion_time_el.name = `round_completion_time[${n_iterations+1-n_iterations_remaining}]`
  const date = new Date();
  round_completion_time_el.value = `${date.getTime()}`;
  frm.appendChild(round_completion_time_el)

  const selected_indices = selected.reduce(
    (out, bool, index) => bool ? out.concat(index) : out, 
    []
  )

  const selected_el = document.createElement("input")
  selected_el.type = "hidden"
  selected_el.name = `selected[${n_iterations+1-n_iterations_remaining}]`
  selected_el.value = JSON.stringify(selected_indices)
  frm.appendChild(selected_el)
  
  let outcomes = document.getElementById('outcomes_estimated')
  outcomes.innerHTML = `Estimated points: ${perceived_utility.toFixed(0)}`
  outcomes = document.getElementById('outcomes_actual')
  outcomes.innerHTML = `Actual points: ${true_utility.toFixed(0)}`
  const cumulative_points_el = document.getElementById('cumulative_points')
  cumulative_points_el.innerHTML = `Cumulative points: ${cumulative_points}`
  const cumulative_bonus_el = document.getElementById('cumulative_bonus')
  cumulative_bonus_el.innerHTML = `Cumulative bonus: \$${cumulative_bonus.toFixed(2)}`

}

function submit() {
  disable_select = true
  let btn = document.getElementById("btn_submit")
  btn.onclick = ""
  const selected_indices = selected.reduce(
    (out, bool, index) => bool ? out.concat(index) : out, 
    []
  )
  const date = new Date();
  $.ajax({
    url:"/experiment/iteration/submit",
    type:"GET",
    data: {"selected_array": JSON.stringify(selected_indices), "db_entry_id": db_entry_id, "round_completion_time": date.getTime(), "assignment_id": assignment_id},
    success: update_view,
    error: function(data) {
      console.log("Ajax request failed.")
      console.log(data)
    }
  })
}