<template>
    <div class="login">
        <div id="formular">
            <h2>Přihlášení pro administrátory</h2>
            <div class="input">
                <input type="text" placeholder="Uživatelské jméno" v-model="uziv" required>
                <hr/>
            </div>
            <div class="input">
                <input type="password" placeholder="Heslo" v-model="heslo" required>
                <hr/>
            </div>
            <button type="submit" @click="prihlasit">Přihlásit</button>
            <p id="spatne" ref="spatne">Špatné přihlašovací údaje</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Login",
    data() {
        return {
            uziv: null,
            heslo: null,
        }
    },
    methods: {
        prihlasit() {

            if (this.uziv !== null && this.heslo !== null) {
                axios.post('/login', {
                    name: this.uziv,
                    password: this.heslo
                }).then(response => {
                    if (response.data.token) { // pokud jsme dostali token
                        localStorage.setItem('token', response.data.token)
                        this.$emit('probehloPrihlaseni', true)
                    } else {
                        this.$refs.spatne.style.display = 'block'
                    }
                })
            } else {

            }
        }
    }
}
</script>

<style scoped>
.login {
    margin-top: 50px;
    font-family: Inter, sans-serif;
}

#formular {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    width: 380px;
    gap: 20px;
    border-radius: 10px;
    box-shadow: 0 10px 30px 10px rgba(0, 0, 0, 0.1);
}

.login input {
    width: 100%;
    padding: 5px;
    background-color: var(--bila);
    border-radius: 5px;
    font-family: inherit;
    border: none;
}

.login input:focus {
    outline: none;
}

.login button {
    width: 100px;
    height: 35px;
    background-color: var(--modra);
    color: var(--bila);
    border: none;
    border-radius: 50px;
    font-family: inherit;
    cursor: pointer;
}

.login hr {
    width: 100%;
    height: 1px;
    border-left: none;
}

#spatne {
    display: none;
    color: red;
}
</style>