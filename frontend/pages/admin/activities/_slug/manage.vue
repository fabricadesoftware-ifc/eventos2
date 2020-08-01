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
                    name: 'admin-activities-slug-edit',
                    params: { slug: activityLocalized.slug }
                  })
                "
                >{{
                  $t('pages.admin-activities-slug-manage.editButton')
                }}</b-button
              >
            </div>
          </div>
          <b-message :type="openStatus.messageType">{{
            openStatus.message
          }}</b-message>
          <h2 class="title is-4">
            {{
              $tc(
                'pages.admin-activities-slug-manage.registrationCount',
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
    const activity = await app.$api.activity.getBySlug(params.slug)
    if (store.state.locale === 'en' && activity.name_english) {
      activity.name = activity.name_english
      delete activity.name_english
    }

    const registrations = await app.$api.activity
      .listRegistrations(activity.slug)
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
          label: this.$t('pages.admin-activities-slug-manage.labels.name'),
          sortable: true
        },
        {
          field: 'user.email',
          label: this.$t('pages.admin-activities-slug-manage.labels.email'),
          sortable: true
        }
      ]
    },
    openStatus() {
      const startsOn = this.$dayjs(this.activityLocalized.starts_on)
      const endsOn = this.$dayjs(this.activityLocalized.ends_on)
      const now = this.$dayjs()

      const isOpen = now.isBetween(startsOn, endsOn)
      const willOpen = now.isBefore(startsOn)

      const status = isOpen ? 'isOpen' : willOpen ? 'willOpen' : 'wasOpen'
      const messagePath = `pages.admin-activities-slug-manage.status.${status}`

      return {
        message: this.$t(messagePath, {
          startDate: startsOn.format('LLLL'),
          endDate: endsOn.format('LLLL')
        }),
        messageType: isOpen ? 'is-success' : willOpen ? 'is-info' : 'is-warning'
      }
    }
  }
}
</script>
