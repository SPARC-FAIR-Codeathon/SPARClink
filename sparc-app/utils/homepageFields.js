/**
 * Get homepage fields, but default to empty values
 * @param {Object} field
 * @returns {Object}
 */
export default (fields = {}) => {
  return {
    heroHeading: fields.heroHeading || '',
    heroCopy: fields.heroCopy || '',
    heroButtonLabel: fields.heroButtonLabel || '',
    heroImage: fields.heroImage || {},
    heroButtonLink: fields.heroButtonLink || '',
    featuredData: fields.featuredData || [],
    newsAndEvents: fields.newsAndEvents || [],
    testimonials: fields.testimonials || [],
    title: fields.title || ''
  }
}
