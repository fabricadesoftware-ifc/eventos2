<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <h1 class="title">{{ $t('pages.admin-eventDetails.title') }}</h1>
          <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(onSubmit)">
              <div v-visible="!loading" class="field">
                <b-message v-if="error" type="is-danger">
                  {{ error }}
                </b-message>
                <b-message v-else type="is-info">
                  {{ $t('pages.admin-eventDetails.description') }}
                </b-message>
              </div>

              <e-input
                v-model="form.name"
                name="name"
                :label="$t('forms.labels.eventName')"
                rules="required"
              />
              <e-input
                v-model="form.name_english"
                name="name_english"
                :label="$t('forms.labels.eventNameInEnglish')"
              />
              <e-input
                v-model="form.slug"
                name="slug"
                :label="$t('forms.labels.eventSlug')"
              />
              <e-datetimepicker
                v-model="form.starts_on"
                name="starts_on"
                :label="$t('forms.labels.eventStartDate')"
              ></e-datetimepicker>
              <e-datetimepicker
                v-model="form.ends_on"
                name="ends_on"
                :label="$t('forms.labels.eventEndDate')"
              ></e-datetimepicker>

              <div class="field">
                <div class="control">
                  <b-button
                    type="is-primary is-pulled-right"
                    native-type="submit"
                    icon-left="arrow-right"
                    :loading="loading"
                    >{{ $t('pages.admin-eventDetails.submitButton') }}</b-button
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
  layout: 'admin',
  mixins: [errorMixin],

  data() {
    return {
      error: null,
      loading: false,
      form: {
        name: '',
        name_english: '',
        slug: '',
        starts_on: new Date(),
        ends_on: new Date()
      }
    }
  },
  created() {
    const event = this.$store.state.event
    this.form.name = event.name
    this.form.name_english = event.name_english
    this.form.starts_on = new Date(event.starts_on)
    this.form.ends_on = new Date(event.ends_on)
    this.form.slug = event.slug
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.$store
        .dispatch('admin/updateEvent', this.form)
        .catch(this.handleGenericError)
        .finally(() => (this.loading = false))
    }
  }
}
</script>
