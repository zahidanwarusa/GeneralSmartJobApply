// Vanilla JS TodoList (add / toggle / delete). Include this after jQuery/bootstrap scripts.
(function () {
  "use strict";

  const initialTasks = [
    { id: 1, text: "This is an example of task #1", completed: true },
    { id: 2, text: "This is an example of task #2", completed: false },
    { id: 3, text: "This is an example of task #3", completed: true },
    { id: 4, text: "This is an example of task #4", completed: false },
    { id: 5, text: "This is an example of task #5", completed: false },
    { id: 6, text: "This is an example of task #6", completed: true }
  ];

  document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("todoInput");
    const addBtn = document.getElementById("todoAddBtn");
    const list = document.getElementById("todoItems");
    if (!input || !addBtn || !list) return;

    // try load from localStorage, otherwise use initial
    let tasks = (() => {
      try {
        const json = localStorage.getItem("todoTasks");
        return json ? JSON.parse(json) : initialTasks.slice();
      } catch (e) {
        return initialTasks.slice();
      }
    })();

    function save() {
      try { localStorage.setItem("todoTasks", JSON.stringify(tasks)); } catch (e) {}
    }

    function render() {
      list.innerHTML = "";
      if (tasks.length === 0) {
        const li = document.createElement("li");
        li.className = "list-group-item text-muted";
        li.textContent = "No tasks yet.";
        list.appendChild(li);
        return;
      }

      tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex align-items-center justify-content-between";

        const left = document.createElement("div");
        left.className = "d-flex align-items-center gap-2";

        const chk = document.createElement("input");
        chk.type = "checkbox";
        chk.className = "form-check-input";
        chk.checked = !!task.completed;
        chk.addEventListener("change", () => toggleTask(task.id));

        const span = document.createElement("span");
        span.textContent = task.text;
        if (task.completed) span.style.textDecoration = "line-through";

        left.appendChild(chk);
        left.appendChild(span);

        const delBtn = document.createElement("button");
        delBtn.type = "button";
        delBtn.className = "btn btn-link text-danger px-0 text-decoration-none";
        delBtn.innerHTML = '<i class="bx bx-x fs-5 p-0"></i>';
        delBtn.addEventListener("click", () => deleteTask(task.id));

        li.appendChild(left);
        li.appendChild(delBtn);
        list.appendChild(li);
      });
    }

    function addTask() {
      const text = (input.value || "").trim();
      if (!text) return;
      tasks.push({ id: Date.now(), text, completed: false });
      input.value = "";
      save();
      render();
      input.focus();
    }

    function toggleTask(id) {
      tasks = tasks.map(t => (t.id === id ? { ...t, completed: !t.completed } : t));
      save();
      render();
    }

    function deleteTask(id) {
      tasks = tasks.filter(t => t.id !== id);
      save();
      render();
    }

    // Event handlers
    addBtn.addEventListener("click", addTask);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") addTask();
    });

    // initial render
    render();
  });
})();