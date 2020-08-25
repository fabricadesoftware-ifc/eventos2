<template>
  <div class="container">
    <div class="columns is-gapless is-centered">
      <div class="column is-5">
        <main class="section">
          <h1 class="title">{{ $t('pages.login.title') }}</h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <e-input
                v-model="form.email"
                name="email"
                type="email"
                :label="$t('forms.labels.email')"
                rules="email|required"
              />
              <e-input
                v-model="form.password"
                name="password"
                type="password"
                :label="$t('forms.labels.password')"
                rules="required"
                password-reveal
              />
              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-fullwidth"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{ $t('pages.login.submitButton') }}</b-button
                  >
                </div>
              </div>
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.login.description') }}
                </b-message>
              </div>
            </form>
          </ValidationObserver>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import errorMixin from '~/mixins/errorMixin'

export default {
  auth: false,
  mixins: [errorMixin],

  data() {
    return {
      error: null,
      loading: false,
      form: {
        email: '',
        password: ''
      }
    }
  },

  methods: {
    onSubmit() {
      this.loading = true
      this.$store
        .dispatch('loginUser', this.form)
        .then(() => {
          this.error = null
          this.$auth.redirect('home')
        })
        .catch(this.handleGenericError)
        .finally(() => (this.loading = false))
    }
  }
}
</script>
