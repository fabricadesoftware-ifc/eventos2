<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">
            {{ $t('pages.admin-tracks-new.title') }}
          </h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-tracks-new.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.trackName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.trackNameInEnglish')"
                rules="required"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.trackStartDate')"
                rules="required"
              ></e-datetimepicker>
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.trackEndDate')"
                rules="required"
              ></e-datetimepicker>

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    icon-left="plus"
                    :loading="loading"
                    @click="$refs.form.handleSubmit(onSubmit)"
                    >{{ $t('pages.admin-tracks-new.submitButton') }}</b-button
                  >
                </div>
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
  mixins: [errorMixin],
  layout: 'admin',

  data() {
    return {
      loading: false,
      error: null,
      form: {
        name: '',
        name_english: '',
        starts_on: new Date(),
        ends_on: new Date()
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$api.track
        .create({ eventSlug: this.$store.state.event.slug, ...this.form })
        .then(() =>
          this.$router.push(this.localePath({ name: 'admin-tracks' }))
        )
        .catch(this.handleGenericError)
        .finally(() => (this.loading = false))
    }
  }
}
</script>
