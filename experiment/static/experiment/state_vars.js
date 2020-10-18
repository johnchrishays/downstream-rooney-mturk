// Parse variables
const n_x = parseInt(document.getElementById('n_x').textContent)
const n_y = parseInt(document.getElementById('n_y').textContent)
const k = parseInt(document.getElementById('k').textContent)
const l = parseInt(document.getElementById('l').textContent)
const bias = JSON.parse(document.getElementById('bias').textContent)
let n_iterations = parseInt(document.getElementById('n_iterations').textContent)
let n_iterations_remaining = n_iterations
let is_x = JSON.parse(document.getElementById('is_x').textContent)
let db_entry_id = JSON.parse(document.getElementById('db_entry_id').textContent)
let round_completion_time = JSON.parse(document.getElementById('round_completion_time').textContent)

const assignment_id = JSON.parse(document.getElementById('assignment_id').textContent)
const hit_id = JSON.parse(document.getElementById('hit_id').textContent)
const worker_id = JSON.parse(document.getElementById('worker_id').textContent)
const pts_per_dollar = parseInt(document.getElementById('pts_per_dollar').textContent)

const is_restore = JSON.parse(document.getElementById('is_restore').textContent)
const selected_restore = JSON.parse(JSON.parse(document.getElementById('selected_restore').textContent))
const db_entry_id_restore = JSON.parse(JSON.parse(document.getElementById('db_entry_id_restore').textContent))
const round_completion_time_restore = JSON.parse(JSON.parse(document.getElementById('round_completion_time_restore').textContent))
const true_utility_restore = JSON.parse(JSON.parse(document.getElementById('true_utility_restore').textContent))
