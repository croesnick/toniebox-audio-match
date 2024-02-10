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
  margin-right: 5px;


}

.btn-danger:hover {
  background-color: #c82333;
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.btn-success {
  background-color: #28a745;
  color: white;
  margin-right: 5px;
}

.btn-success:hover {
  background-color: #218838;
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.btn-outline-secondary {
  background-color: transparent;
  color: #6c757d;
  border: 1px solid #6c757d;
  padding: 0.375rem 1.25rem;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  margin-right: 5px;
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
  margin-right: 5px;
}

.input-group .form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
}

.dropdown {
  max-width: 40%;
  background-color: darkolivegreen;
}

.dropdown-container {
  margin-top: 10px;
  display: flex;
  justify-content: center;
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
  margin-top: 1.5rem;
  margin-right: 0.2rem;
  margin-left: -1rem;
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

.info-box {
    border: 1px solid #fff; /* Change color as needed */
    padding: 10px;
    margin-bottom: 20px; /* Adjust as needed for spacing */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Optional: for subtle shadow */
    background-color: #696a76; /* Change color as needed (match your UI theme) */
    color: #fff; /* Text color */
    border-radius: 5px; /* Optional: if you want rounded corners */
}

.info-box span {
    display: block; /* Makes each span take the full width */
    text-align: left; /* Align text to the left if that fits your design */
    margin-bottom: 5px; /* Space out the lines */
}

.center-text {
  text-align: center;
  margin-bottom: 10px;
}
</style>
