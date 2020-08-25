function getSingleFieldError(error) {
  if (!error.fields) {
    return
  }
  const fieldKeys = Object.keys(error.fields)
  if (fieldKeys.length === 1) {
    return error.fields[fieldKeys[0]].join('\n')
  }
}
function showError(message, error) {
  if (this.error !== undefined) {
    this.error = message
  }
  if (this.$refs.form) {
    this.$refs.form.setErrors(error.fields)
  } else {
    // Se existe só um campo com erro, usá-lo como mensagem de erro.
    message = getSingleFieldError(error) || message
    this.$buefy.toast.open({
      duration: 5000,
      message,
      position: 'is-bottom-right',
      type: 'is-danger'
    })
  }
}

export default {
  methods: {
    handleGenericError(error) {
      let message = this.$t('genericErrors.network')

      if (error.name === 'APIValidationError') {
        message = error.message || this.$t('genericErrors.formValidation')
      } else if (
        error.name === 'APIError' ||
        (error.response && error.response.status === 500)
      ) {
        message = this.$t('genericErrors.api')
      }

      showError.call(this, message, error)
    }
  }
}
