<template>
  <v-container fluid>
    <v-layout row wrap>
      <YNPanel :func="ynpanel.function" @no="ynpanel.visible = false" :visible="ynpanel.visible" :header="ynpanel.header" :text="ynpanel.text"></YNPanel>
      <v-flex xs12>
        <v-layout row justify-end wrap>
          <v-flex xs6 sm3 md2 lg1>
            <v-btn slot="activator" @click="open_create_dialog()" prepend-icon flat color="green"><v-icon>add</v-icon>Добавить</v-btn>
            <v-dialog
              v-model="dialog.visible"
              persistent :overlay="false"
              max-width="500px"
              transition="dialog-transition"
            >
              <v-card>
                <v-card-title class="headline">
                  <p>{{dialog.header}}</p>
                </v-card-title>
                <v-card-text>
                  <v-form ref="form">
                    <v-layout row wrap>

                      <v-flex xs12>
                        <v-text-field
                          :rules="[rules.required]"
                          label="Наименование"
                          color="orange"
                          v-model="temp_data.name"
                          prepend-icon="work"
                        ></v-text-field>
                      </v-flex>

                      <v-flex xs12>
                        <v-textarea
                          :rules="[rules.required]"
                          label="Описание"
                          color="orange"
                          v-model="temp_data.text"
                          prepend-icon="comment"
                        ></v-textarea>
                      </v-flex>

                      <v-flex v-for="link in temp_data.links" xs12>
                        <v-layout row wrap>
                          <v-flex xs12 md6>
                            <v-text-field
                              :rules="[rules.required]"
                              append-outer-icon="clear"
                              label="Сайт"
                              color="orange"
                              prepend-icon="language"
                              @click:append-outer="delete_link(link)"
                              v-model="link.link"
                            ></v-text-field>
                          </v-flex>
                          <v-flex xs12>
                            <v-text-field
                              :rules="[rules.required]"
                              label="Комментарий"
                              color="orange"
                              prepend-icon="comment"
                              v-model="link.comment"
                            ></v-text-field>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex xs12 md6 offset-md3>
                        <v-btn block flat color="green" @click="add_link()">+ Сайт</v-btn>
                      </v-flex>

                      <v-flex v-for="media in temp_data.media" xs12>
                        <v-layout row wrap>
                          <v-flex xs12 md6>
                            <v-text-field
                              :rules="[rules.required]"
                              append-outer-icon="clear"
                              label="Ссылка на файл"
                              color="orange"
                              prepend-icon="attachment"
                              @click:append-outer="delete_media(media)"
                              v-model="media.link"
                            ></v-text-field>
                          </v-flex>
                          <v-flex xs12>
                            <v-text-field
                              :rules="[rules.required]"
                              label="Комментарий"
                              color="orange"
                              prepend-icon="comment"
                              v-model="media.comment"
                            ></v-text-field>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex xs12 md6 offset-md3>
                        <v-btn block flat color="green" @click="add_media()">+ Медиа</v-btn>
                      </v-flex>

                    </v-layout>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-layout justify-end text-xs-center row wrap>
                    <v-flex md3 xs6>
                      <v-btn flat color="red" @click="dialog.visible = false"><p>Закрыть</p></v-btn>
                    </v-flex>
                    <v-flex md3 xs6>
                      <v-btn flat color="green" @click="dialog.confirm_function()"><p>Сохранить</p></v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-actions>
              </v-card>
            </v-dialog>

          </v-flex>
        </v-layout>
      </v-flex>

      <v-flex pa-2 md4 lg3 sm6 xs12 v-for="(row, index) in data" :key="index" pt-2>
        <v-card pa-4 hover class="rounded">

          <v-card-text class="pa-0" @click="row.info = !row.info">
            <div style="display: flex; flex-direction: column;float: right;">
              <div><v-btn small @click="delete_data(row)" icon><v-icon small color="red">close</v-icon></v-btn></div>
              <div><v-btn small @click="open_edit_dialog(row)" icon><v-icon small color="primary">edit</v-icon></v-btn></div>
            </div>
            <v-layout class="pa-2" row wrap>
                <v-flex xs12 class="headline">
                  <p>{{ row.name }}</p>
                </v-flex>
                <v-flex xs12>
                  <p>{{ row.text }}</p>
                </v-flex>
            </v-layout>
          </v-card-text>

        <v-card-actions  style="width: 100%; background-color:rgba(240,240,240,0.5)" v-show="row.info">
          <v-layout pa-2 row wrap>
            <v-flex xs12 class="headline">
              <p>Ссылки по делу:</p>
            </v-flex>
            <v-flex v-for="link in row.links">
              <div><p><a target="_blank" :href="(link.link.match(/http/i)? link.link : 'http://' + link.link)">{{ link.link }}</a></p></div>
              <div><p>{{ link.comment }}</p></div>
            </v-flex>
            <v-flex pt-4 xs12 class="headline">
              <p>Материалы по делу:</p>
            </v-flex>
            <v-flex v-for="link in row.media">
              <div><p><a target="_blank" :href="(link.link.match(/http/i)? link.link : 'http://' + link.link)">Файл</a></p></div>
              <div><p>{{ link.comment }}</p></div>
            </v-flex>
          </v-layout>
        </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import YNPanel from '../components/YNPanel.vue'
import axios from 'axios'

  export default {
    components:{YNPanel},
    methods:{
      save_data(){
        if(this.$refs.form.validate()){
          var data = {
            department: "Фильтрация",
            data: this.temp_data
          }
          delete data.data.info
          axios.post('https://ocheredsut.ru/api/1/deps/', data).then((resp) =>{
            var data = resp.data.data
            data.id = resp.data.id
            data.info = false
            this.data.push(data)
            this.dialog.visible = false
          })
        }
      },
      open_create_dialog(){
        var a = {
          name: "",
          info: false,
          links: [
            {
              link: "",
              comment: ""
            }
          ],
          text: "",
          media: [
            {
              link: "",
              comment: ""
            }
          ]
        }
        this.temp_data = a;
        this.dialog.confirm_function = this.save_data
        this.dialog.visible = true
      },
      add_link(){
        this.temp_data.links.push(
          {
            link: "",
            comment: ""
          }
        )
      },
      add_media(){
        this.temp_data.media.push(
          {
            link: "",
            comment: ""
          }
        )
      },
      delete_link(link){
        this.temp_data.links.splice(this.temp_data.links.indexOf(link), 1)
      },
      delete_media(media){
        this.temp_data.media.splice(this.temp_data.media.indexOf(media), 1)
      },
      delete_data(data){
        this.ynpanel = {
          header: data,
          visible: true,
          text: 'Удалить дело?'
        }
        this.ynpanel.function = (d => {
          axios.delete('https://ocheredsut.ru/api/1/deps/' + d.id).then((resp)=>{
            this.data.splice(this.data.indexOf(d), 1)
          })
        })

      },
      edit_save(){
        if(this.$refs.form.validate()){
            const data = {
              data: Object.assign({}, this.temp_data),
            }
            delete data.data.id
            delete data.data.info
            axios.put('https://ocheredsut.ru/api/1/deps/'+this.temp_data.id, data).then((resp) =>{
              var temp = resp.data.data
              temp.id = resp.data.id
              var ind = this.data.findIndex(a=>{return a.id === temp.id})
              this.data[ind] = temp
              this.dialog.visible = false;
            })
        }
      },
      open_edit_dialog(row){
        var t = Object.assign({}, row)
        this.temp_data = t;
        this.dialog.confirm_function = this.edit_save
        this.dialog.visible = true
      },
    },
    created(){
      axios.get('https://ocheredsut.ru/api/1/deps/', {params:{department: "Фильтрация"}}).then((resp)=>{
        this.data = resp.data.data.map(a=>{a.data.id = a.id; a.data.info = false; return a.data})
      })
    },
    data(){
      return {
        ynpanel: {
          visible: false,
          header: '',
          text: ''
        },
        dialog: {
          visible: false,
          confirm_function: null,
          header: ""
        },
        rules: {
          required: value => !!value.replace(/\s+/,'')  || 'Обязательное поле',
          min: v => v.length >= 8 || 'Минимум 8 букв'
        },
        temp_data: {
          name: "",
          info: false,
          links: [
            {
              link: "",
              comment: ""
            }
          ],
          text: "",
          media: []
        },
        data: []
      }
    }
  }
</script>

<style>
</style>
