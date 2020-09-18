export function createDocumentAPIClient($axios) {
  return {
    create({ file }) {
      const formData = new FormData()
      formData.append('file', file)
      return $axios.$post(`api/v1/documents/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
  }
}
