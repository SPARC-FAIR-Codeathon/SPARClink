/**
 * Success notification message object
 * @param {String} message
 * @return {Object}
 */
export const successMessage = message => {
  return {
    message: message,
    showClose: true,
    iconClass: 'el-icon-circle-check',
    customClass: 'el-message--success',
    duration: 5000
  }
}
/**
 * Failure notification message object
 * @param {String} message
 * @return {Object}
 */
export const failMessage = message => {
  return {
    message: message,
    showClose: true,
    iconClass: 'el-icon-circle-close',
    customClass: 'el-message--error',
    duration: 5000
  }
}
