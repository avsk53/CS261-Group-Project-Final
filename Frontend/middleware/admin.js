export default function ({ store, redirect }) {
    if (store.state.auth.loggedIn && store.state.auth.user.role_id !== 0) {
      return redirect('/dashboard')
    }else if (!store.state.auth.loggedIn) {
      return redirect('/')
    }
  }