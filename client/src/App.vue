<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Button Enhancements */
.btn {
  border: none;
  border-radius: 4px;
  padding: 0.625rem 1.25rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: none; /* Remove shadow for a flatter design */
}


.btn:hover {
  transform: translateY(-2px); /* subtle lift effect on hover */
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.btn-outline-secondary {
  background-color: transparent;
  color: #6c757d;
  border: 1px solid #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0069d9;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

/* Input Field Enhancements */
.input-group .form-control {
  border-radius: 4px;
  border: 2px solid #ced4da;
  padding: 0.625rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-group .form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
}

/* Container and Row Enhancements for better spacing */
.container {
  padding: 20px;
}

.row {
  margin-bottom: 20px;
}

/* Checkbox Enhancement */
.form-check-input {
  margin-top: 0.3rem;
  margin-right: 0.5rem;
  cursor: pointer;
}

/* General Text and Placeholder Enhancements */
.text-muted {
  color: #6c757d;
}

::placeholder {
  color: #adb5bd;
  opacity: 1; /* Firefox */
}

/* Responsive Typography */
@media (min-width: 768px) {
  .bd-placeholder-img-lg {
      font-size: 3.5rem;
  }
  h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
  }
}

/* Typography Enhancements */
.list-group-item strong {
  display: block;
  font-size: 1.25rem; /* Larger font size for title */
  margin-bottom: 0.25rem;
}

.list-group-item small {
  font-size: 0.875rem; /* Smaller font size for details */
}


/* Hover effect for list items */
.list-group-item:hover {
  background-color: #f8f9fa;
}

/* List Group Item Enhancement */
.list-group-item {
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  transform: scale(1.02); /* subtle scale effect on hover */
}
</style>
