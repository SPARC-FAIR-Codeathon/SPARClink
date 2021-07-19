export default function(context) {
  context.hasAgreedToCookie = context.$cookies.get('cookie-name')
}
