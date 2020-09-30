<template>
  <div class="container">
    <div class="columns is-gapless is-10">
      <div class="column">
        <main class="section">
          <div class="columns is-gapless">
            <div class="column">
              <h1 class="title is-3">{{ activityLocalized.name }}</h1>
            </div>
            <div class="column is-narrow">
              <b-button
                type="is-primary"
                tag="nuxt-link"
                :to="
                  localePath({
                    name: 'admin-activities-id-edit',
                    params: { id: activityLocalized.id }
                  })
                "
                >{{
                  $t('pages.admin-activities-id-manage.editButton')
                }}</b-button
              >
            </div>
          </div>
          <b-message
            :type="activityLocalized.is_open ? 'is-success' : 'is-info'"
            >{{ statusMessage }}</b-message
          >
          <h2 class="title is-4">
            {{
              $tc(
                'pages.admin-activities-id-manage.registrationCount',
                registrations.length
              )
            }}
          </h2>
          <b-table
            v-if="registrations.length"
            :data="registrations"
            :columns="registrationColumns"
            default-sort="user.fullName"
          />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'admin',
  async asyncData({ app, params, store }) {
    const activity = await app.$api.activity.getById(params.id)
    if (store.state.locale === 'en' && activity.name_english) {
      activity.name = activity.name_english
    }
    delete activity.name_english

    const registrations = await app.$api.activity
      .listRegistrations(activity.id)
      .then(registrations =>
        registrations.map(registration => ({
          ...registration,
          user: {
            ...registration.user,
            fullName:
              registration.user.first_name + ' ' + registration.user.last_name
          }
        }))
      )
    return {
      activityLocalized: activity,
      registrations
    }
  },
  computed: {
    registrationColumns() {
      return [
        {
          field: 'user.fullName',
          label: this.$t('pages.admin-activities-id-manage.labels.name'),
          sortable: true
        },
        {
          field: 'user.email',
          label: this.$t('pages.admin-activities-id-manage.labels.email'),
          sortable: true
        }
      ]
    },
    statusMessage() {
      const startsOn = this.$dayjs(this.activityLocalized.starts_on)
      const endsOn = this.$dayjs(this.activityLocalized.ends_on)

      const isOpen = this.activityLocalized.is_open
      const willOpen = this.$dayjs().isBefore(startsOn)

      const status = isOpen ? 'isOpen' : willOpen ? 'willOpen' : 'wasOpen'
      const messagePath = `pages.admin-activities-id-manage.status.${status}`
      return this.$t(messagePath, {
        startDate: startsOn.format('LLLL'),
        endDate: endsOn.format('LLLL')
      })
    }
  }
}
</script>
