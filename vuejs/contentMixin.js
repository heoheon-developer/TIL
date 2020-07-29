import moment from 'moment/moment'

export const contentMixin = {

  data() {

    return {
      selectFolder: [],
      selectFile: [],
    }
  },

  methods: {
    fmtDate(value) {
      if (value) {
        return moment(String(value)).format('YYYY.MM.DD HH:mm:ss')
      }
    },
    fmtDateOnly(value) {
      if (value) {
        return moment(String(value)).format('YYYY-MM-DD')
      }
    },
    kstDate(value) {
      if (value) {
        return moment(String(value)).add(9, 'H').format('YYYY.MM.DD HH:mm:ss')
      }
    },
    formatFileSize(size) {
      if (size == null)
        return '-'

      var i = -1;
      var byteUnits = [' KB', ' MB', ' GB', ' TB', 'PB', 'EB', 'ZB', 'YB'];
      do {
        size = size / 1024;
        i++;
      } while (size > 1024);

      return Math.max(size, 0.1).toFixed(1) + byteUnits[i];
    },

    onContextMenu(e, objAuth) {
      e.preventDefault();
      var posX = e.clientX;
      var posY = e.clientY;
      var contextMenu = $(".menu_layer");

      let menuLen = 0;

      $.each(objAuth, function (key, value) {
        if (value)
          menuLen += 1
      });

      if (menuLen < 1)
        return;

      let menuHeight = menuLen * 29;

      if ($(window).height() - menuHeight < posY) {
        posY -= menuHeight
      }
      contextMenu.css({
        "display": "block",
        "position": "fixed",
        "top": posY + "px",
        "left": posX + "px",
        "z-index": 3
      });

      $("html,body").on("click", function (e) {
        contextMenu.hide();
      })
    },


    fileDownLoad(item) {

      this.selectFile.push(item)

      let folders = this.selectFolder
      let files = this.selectFile
      let fileName = ''

      console.log("files===>", files)


      if (folders.length < 1 && files.length == 1) {
        fileName = files[0].fi_name
      } else {

        fileName = "AOSBOX.zip"
      }

      folders = folders.map(m => m.fi_id)
      files = files.map(m => m.fi_id)

      let tempPath = this.makeGuid()

      console.log("file_down", files)

      var qs = require('qs');

      axios.post('/storage_service/downloadFile/',
        qs.stringify({
          folders: JSON.stringify(folders),
          files: JSON.stringify(files),
          tempPath: tempPath
        }),
        {
          responseType: 'blob'
        }).then(result => {
        if (result.headers['content-type'] != 'application/json') {
          let blob = new Blob([result.data], {type: result.headers['content-type']})
          let link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = fileName
          link.click()
        }
        this.deleteTempPath(tempPath)

      }).catch(error => {
        console.log(error)
      })
      this.selectFile = []
    },

    deleteTempPath(tempPath) {

      var qs = require('qs');

      axios.post('/storage_service/deleteTempPath/',
        qs.stringify({
          tempPath: tempPath
        })
      ).then(result => {

      }).catch(error => {

        console.log(error)
      })
    },


    makeGuid() {
      function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
          .toString(16)
          .substring(1);
      }

      return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
    },
  }
}

