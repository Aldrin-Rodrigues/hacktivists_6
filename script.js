<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zero</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</head>
<body>
    <header>
        <h1>Zero.</h1>
    </header>

    <div class="container">
        <!-- First Division -->
        <div class="division division-left">
            <!-- Subdivision 1: Document Options -->
            <div class="subdivision">
              <p>What document do you want to upload:</p>
          
              <label for="aadharBtn">
                  <input type="radio" id="aadharBtn" name="document" value="Aadhar Card">
                  Aadhar Card
              </label>
          
              <label for="panBtn">
                  <input type="radio" id="panBtn" name="document" value="PAN Card">
                  PAN Card
              </label>
          
              <label for="vaccineBtn">
                  <input type="radio" id="vaccineBtn" name="document" value="Covid-19 Vaccination Certificate">
                  Covid-19 Vaccination Certificate
              </label>
          </div>
          
          <!-- Subdivisions for the radio button-specific dropdowns -->
          <div class="subdivision" id="aadharDropdown" style="display: none;">
              <p>Aadhar Card Options:</p>
              <select>
                  <option value="age">Age Verification</option>
                  <option value="address">Address Verification</option>
                  <option value="aadharNumber">Valid Aadhar Number</option>
              </select>
          </div>
          
          <div class="subdivision" id="panDropdown" style="display: none;">
              <p>PAN Card Options:</p>
              <select>
                  <option value="age">Age Verification</option>
                  <option value="citizenship">Citizenship Verification</option>
              </select>
          </div>
          
          <div class="subdivision" id="vaccineDropdown" style="display: none;">
              <p>Covid-19 Vaccination Certificate Options:</p>
              <select>
                  <option value="vaccineVerification">Verify Covid-19 Vaccine</option>
              </select>
          </div>          

            <!-- Subdivision 2: Upload Option -->
            <div class="subdivision">
                <p>Upload your document:</p>
                <input type="file" id="uploadInput" accept=".pdf,.jpg,.png">
            </div>
<!--
            <div class="dropdown-menu d-block position-static rounded-4 shadow overflow-hidden custom-width" data-bs-theme="dark">
                <form class="p-2 mb-2 bg-dark border-bottom border-dark">
                  <input type="search" class="form-control bg-dark" autocomplete="false" placeholder="Choose document . .">
                </form>
                <ul class="list-unstyled mb-0">
                  <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
                    <span class="d-inline-block bg-success rounded-circle p-1"></span>
                    Age verification
                  </a></li>
                  <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
                    <span class="d-inline-block bg-primary rounded-circle p-1"></span>
                    Aadhar verification
                  </a></li>
                  <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
                    <span class="d-inline-block bg-danger rounded-circle p-1"></span>
                    Pan verification
                  </a></li>
                  <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
                    <span class="d-inline-block bg-info rounded-circle p-1"></span>
                    COVID Vaccince verification
                  </a></li>
                </ul>
        </div>
      -->
            <!-- Subdivision 4: Age Limit -->
            <div class="subdivision">
                <p>Enter Age Limit (18 or 21):</p>
                <input type="text" id="ageLimit" placeholder="Type 18 or 21">
            </div>
        </div>

        <!-- Second Division: Display Uploaded Document -->
        <div class="division division-right">
            <p>Uploaded document preview will appear here:</p>
            <iframe id="documentPreview" width="100%" height="400px"></iframe>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
