document.addEventListener("DOMContentLoaded", function() { const themeToggleBtn = document.getElementById("theme-toggle"); themeToggleBtn.addEventListener("click", function() { document.body.classList.toggle("dark-mode"); }); function renderTodos() { const todoList = document.getElementById("todo-list"); todoList.innerHTML = ""; tasks.forEach((task, index) => { const li = document.createElement("li"); li.textContent = task; const deleteBtn = document.createElement("button"); deleteBtn.textContent = "Delete"; deleteBtn.addEventListener("click", () => { deleteTask(index); }); const editBtn = document.createElement("button"); editBtn.textContent = "Edit"; editBtn.addEventListener("click", () => { const updatedTask = prompt("Edit task:", task); if(updatedTask) { updateTask(index, updatedTask); } }); li.appendChild(editBtn); li.appendChild(deleteBtn); todoList.appendChild(li); }); } 

 let tasks = []; 
 function addTask(task) { tasks.push(task); renderTodos(); } 
 function deleteTask(index) { tasks.splice(index, 1); renderTodos(); } 
 function updateTask(index, updatedTask) { tasks[index] = updatedTask; renderTodos(); } 

 document.getElementById("add-todo").addEventListener("click", function() { const newTodoText = document.getElementById("todo-input").value; if(newTodoText) { addTask(newTodoText); document.getElementById("todo-input").value = ""; } }); });
