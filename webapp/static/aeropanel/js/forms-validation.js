// jQuery form validation for forms-layouts.html (basic rules + bootstrap classes)
(function ($) {
  "use strict";

  // helpers
  function setValid($el, msg) {
    $el.removeClass("is-invalid").addClass("is-valid");
    var $fb = $el.siblings(".valid-feedback");
    if ($fb.length) $fb.text(msg || "Looks good!");
  }
  function setInvalid($el, msg) {
    $el.removeClass("is-valid").addClass("is-invalid");
    var $fb = $el.siblings(".invalid-feedback");
    if ($fb.length) $fb.text(msg || "This field is required.");
  }
  function isEmail(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  }
  function isPhone(val) {
    return /^[0-9\-\+\s\(\)]{7,20}$/.test(val);
  }
  function isNumeric(val) {
    return !isNaN(parseFloat(val)) && isFinite(val);
  }

  $(function () {
    // target all forms inside .form-layout-wrapper
    $(".form-layout-wrapper form").each(function () {
      var $form = $(this);

      // live validation on blur/change
      $form.on("blur change input", "input, textarea, select", function (e) {
        var $el = $(this);
        validateField($el);
      });

      // submit handler
      $form.on("submit", function (e) {
        e.preventDefault();
        var valid = true;

        $form.find("input, textarea, select").each(function () {
          if (!validateField($(this))) valid = false;
        });

        if (valid) {
          // submit normally or you can send via ajax
          // $form.off('submit').submit();
          // simple success feedback
          $form.find("button[type=submit]").prop("disabled", true).text("Submitting...");
          setTimeout(function () {
            $form.find("button[type=submit]").prop("disabled", false).text("Submit");
            // show success state for demonstration
            $form[0].reset();
            $form.find(".is-valid").removeClass("is-valid");
            alert("Form validated successfully (demo).");
          }, 600);
        } else {
          // focus first invalid
          $form.find(".is-invalid:first").focus();
        }
      });
    });

    // field validation rules
    function validateField($el) {
      var name = $el.attr("name");
      var val = ($el.val() || "").trim();
      var tag = $el.prop("tagName").toLowerCase();
      var type = $el.attr("type");

      // skip validation for hidden inputs
      if ($el.is(":hidden")) return true;

      // required checks for common names
      var requiredNames = [
        "firstName", "lastName", "email", "phone", "dob",
        "gender", "course", "address", "name", "jobTitle",
        "companyName", "location", "jobType", "experience",
        "salaryMin", "salaryMax", "description", "fullName",
        "city", "state", "zip", "country", "paymentMethod",
        "password"
      ];

      // checkboxes & radios: if name exists and it's required by UI, ensure one selected
      if (type === "checkbox" || type === "radio") {
        // if checkbox has explicit 'name' and the form contains a matching hidden-required control (skip unless present)
        if ($el.closest("form").find("[name='" + name + "']").length > 0 && $el.prop("required")) {
          if (!$el.is(":checked")) {
            setInvalid($el, "This option is required.");
            return false;
          } else {
            setValid($el);
            return true;
          }
        }
        // don't mark inline checkboxes/radios as invalid by default
        return true;
      }

      // required field check
      if (requiredNames.indexOf(name) !== -1) {
        if (!val) {
          setInvalid($el, "This field is required.");
          return false;
        }
      }

      // specific rules
      if (name === "email") {
        if (val && !isEmail(val)) {
          setInvalid($el, "Enter a valid email address.");
          return false;
        }
      }

      if (name === "phone") {
        if (val && !isPhone(val)) {
          setInvalid($el, "Enter a valid phone number.");
          return false;
        }
      }

      if (name === "password") {
        if (val && val.length < 8) {
          setInvalid($el, "Password must be at least 8 characters.");
          return false;
        }
      }

      if (name === "salaryMin" || name === "salaryMax") {
        if (val && !isNumeric(val)) {
          setInvalid($el, "Enter a valid number.");
          return false;
        }
        // if both present, check range
        var $form = $el.closest("form");
        var min = parseFloat($form.find("[name='salaryMin']").val() || "");
        var max = parseFloat($form.find("[name='salaryMax']").val() || "");
        if (!isNaN(min) && !isNaN(max) && min > max) {
          setInvalid($form.find("[name='salaryMin']"), "Min should be <= Max.");
          setInvalid($form.find("[name='salaryMax']"), "Max should be >= Min.");
          return false;
        } else {
          if ($form.find("[name='salaryMin']").val()) setValid($form.find("[name='salaryMin']"));
          if ($form.find("[name='salaryMax']").val()) setValid($form.find("[name='salaryMax']"));
        }
      }

      if (name === "zip") {
        if (val && !/^[A-Za-z0-9\- ]{3,10}$/.test(val)) {
          setInvalid($el, "Enter a valid zip/postal code.");
          return false;
        }
      }

      // checkbox confirmations (e.g., confirm, agree, saveDetails)
      if ((name === "confirm" || name === "agree") && $el.length) {
        if (!$el.is(":checked")) {
          setInvalid($el, "You must confirm to proceed.");
          return false;
        } else {
          setValid($el);
        }
      }

      // default success
      if ($el.val() !== undefined) setValid($el);
      return true;
    }
  });
})(jQuery);