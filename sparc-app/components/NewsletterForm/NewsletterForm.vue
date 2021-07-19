<template>
  <!-- Generated from MailChimp. Docs: https://mailchimp.com/help/add-a-signup-form-to-your-website/ -->
  <div id="mc_embed_signup">
    <form
      id="mc-embedded-subscribe-form"
      action="https://science.us2.list-manage.com/subscribe/post?u=e60c48f231a30b544eed731ea&amp;id=c81a347bd8"
      method="post"
      name="mc-embedded-subscribe-form"
      class="validate"
      target="_blank"
      novalidate
    >
      <div id="mc_embed_signup_scroll">
        <div class="mc-field-group mb-40">
          <label for="mce-FNAME" class="mb-16">First name </label>
          <input
            id="mce-FNAME"
            type="text"
            value=""
            name="FNAME"
            class="input-text"
            placeholder="Enter your first name"
          />
        </div>
        <div class="mc-field-group mb-40">
          <label for="mce-LNAME" class="mb-16">Last name </label>
          <input
            id="mce-LNAME"
            type="text"
            value=""
            name="LNAME"
            class="input-text"
            placeholder="Enter your last name"
          />
        </div>

        <div class="mc-field-group mb-48">
          <label for="mce-EMAIL" class="mb-16">
            Email address
          </label>
          <input
            id="mce-EMAIL"
            type="email"
            value=""
            name="EMAIL"
            class="required email input-text"
            placeholder="Enter your email address"
          />
        </div>
        <div id="mce-responses" class="clear">
          <div id="mce-error-response" class="response" style="display:none" />
          <div
            id="mce-success-response"
            class="response"
            style="display:none"
          />
        </div>
        <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
        <div style="position: absolute; left: -5000px;" aria-hidden="true">
          <input
            type="text"
            name="b_e60c48f231a30b544eed731ea_c81a347bd8"
            tabindex="-1"
            value=""
          />
        </div>
        <div class="clear">
          <div class="clear">
            <input
              id="mc-embedded-subscribe"
              type="submit"
              value="Sign-up"
              name="subscribe"
              class="el-button secondary"
            />
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'NewsletterForm'
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

form,
.mc-field-group {
  display: flex;
  flex-direction: column;
  max-width: 20rem;
}
label {
  font-size: 1.5rem;
}
.input-text {
  border: 1px solid $medium-gray;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  &:focus {
    border-color: $app-primary-color;
  }
}
</style>
