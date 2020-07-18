<template>
  <article id="contents" class="main">
    <div class="main_top_section_wrapper">
      <section id="main_intro">
        <h2>
          <strong>AOSBOXは日本NO.1</strong>の<br/>
          クラウドバックアップ<br/>
          ソリューション
        </h2>
        <p>日本のPC＆スマホをバックアップします</p>
      </section>
      <!-- S : 관리자 모드 -->
      <section id="main_intro" class="vary_admin" style="display:none;">
        <ul class="main_intro_tab">
          <li>
            <a href="http://" class="active">バックアップ状況</a>
          </li>
          <li>
            <a href="http://">バックアップ状況</a>
          </li>
        </ul>
        <div class="bar_graph_wrap">
          <ul class="">
            <li class="bar_color_01">
              <i class="bullet"></i>
              <span>バックアップ状況</span>
            </li>
            <li class="bar_color_02">
              <i class="bullet"></i>
              <span>バックアップ状況</span>
            </li>
          </ul>
          <div class="bar_graph_con">
            <img src="@/assets/images/main/sample_bar_graph.jpg" alt="" class="">
          </div>
        </div>
      </section>
      <!-- E : 관리자 모드 -->
      <section class="main_backup_status circle_graph">
        <div class="mbs_status">
          <h2>バックアップ状況</h2>
          <div class="gauge">


            <apexchart width="300" type="radialBar" :options="options" :series="series"></apexchart>
<!--						<div class="condition safety">-->
<!--							<div class="ico">-->
<!--								<img src="@/assets/images/main/ico_bso_cloud.png" alt="" />-->
<!--							</div>-->
<!--							<p class="txt">未保護</p>-->
<!--						</div>-->


          </div>
          <div class="count">
            <h3>バックアップ状況</h3>
            <p class="condition">未保護</p>
            <p class="desc">あなたの端末のバックアップ状況をご確認ください</p>
            <ul>
              <li class="valid">
                <i class="bullet"></i><span class="category">有効 端末</span>
                <strong class="length">2</strong>
              </li>
              <li class="online">
                <i class="bullet"></i><span class="category">端末がオンライン</span>
                <strong class="length">10</strong>
              </li>
              <li class="backing">
                <i class="bullet"></i><span class="category">端末がバックアップ中</span>
                <strong class="length">110</strong>
              </li>
            </ul>
          </div>
        </div>
      </section>
      <section class="main_backup_status main_backup_status02">
        <div class="mbs_protect">
          <h2>バックアップ状態</h2>
          <ul>
            <li class="completely">
              <h3>保護済み</h3>
              <img src="@/assets/images/main/ico_bsp_completely.png" alt="" class="ico"/>
              <p class="desc">バックアップ率90%以上</p>
              <p class="length">2</p>
            </li>
            <li class="partially">
              <h3>一部保護済み</h3>
              <img src="@/assets/images/main/ico_bsp_partially.png" alt="" class="ico"/>
              <p class="desc">バックアップ率80~90%</p>
              <p class="length">0</p>
            </li>
            <li class="not">
              <h3>未保護</h3>
              <img src="@/assets/images/main/ico_bsp_not.png" alt="" class="ico"/>
              <p class="desc">バックアップ率80%未満</p>
              <p class="length">0</p>
            </li>
            <li class="non_use">
              <h3>不使用</h3>
              <img src="@/assets/images/main/ico_bsp_non_use.png" alt="" class="ico"/>
              <p class="desc">30日以上微動作</p>
              <p class="length">0</p>
            </li>
          </ul>
        </div>
      </section>
    </div>
    <section id="main_situation">
      <div class="storage ms_list">
        <h2>ストレージ使用率</h2>
        <ul>
          <li class="normal">
            <h3>通常のストレ`ージ</h3>
            <div class="gauge">
              <img src="@/assets/images/main/gauge_mss_normal.png" alt="" style="width:110px; height:110px;"/>
              <!-- //임시 그래프 이미지(그래프색상:#F35458) -->
              <img src="@/assets/images/main/ico_mss_normal.png" alt="" class="ico"/>
            </div>
            <p class="used_size"><strong>2.56GB</strong>使用中</p>
            <p class="total_size"><strong>10.00GB</strong>使用中</p>
          </li>
          <li class="cold">
            <h3>コールドストレージ</h3>
            <div class="gauge">
              <img src="@/assets/images/main/gauge_mss_cold.png" alt="" style="width:110px; height:110px;"/>
              <!-- //임시 그래프 이미지(그래프색상:#47A1EE) -->
              <img src="@/assets/images/main/ico_mss_cold.png" alt="" class="ico"/>
            </div>
            <p class="used_size"><strong>2.56GB</strong>使用中</p>
            <p class="total_size"><strong>10.00GB</strong>使用中</p>
          </li>
          <li class="ocr">
            <h3>OCR ページ</h3>
            <div class="gauge">
              <img src="@/assets/images/main/gauge_mss_ocr.png" alt="" style="width:110px; height:110px;"/>
              <!-- //임시 그래프 이미지(그래프색상:#326EA1) -->
              <img src="@/assets/images/main/ico_mss_ocr.png" alt="" class="ico"/>
            </div>
            <p class="used_size"><strong>2.56GB</strong>使用中</p>
            <p class="total_size"><strong>10.00GB</strong>使用中</p>
          </li>
        </ul>
      </div>
      <div class="alim ms_list">
        <h2>状況リスト</h2>
        <ul>
          <li>
            <img src="@/assets/images/main/ico_msa_alim_on.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim_on.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong></span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim_on.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong></span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
          <li>
            <img src="@/assets/images/main/ico_msa_alim.png" alt="" class="ico"/>
            <span class="record">DESKTOP-HB706O8 の <strong class="condition">バックアップ完了</strong> (270.38 MB/866 項目)</span>
            <time datetime="2019-02-28 14:32:33">2 分前</time>
          </li>
        </ul>
      </div>
      <div class="data_type ms_list">
        <h2>データの種類</h2>
        <ul>
          <li>
            <h3>すべてファイル</h3>
            <img src="@/assets/images/main/ico_madt_all.png" alt="" class="ico"/>
            <p class="percentage">100%</p>
            <div class="range">
              <span class="gauge" style="width:100%"></span>
            </div>
          </li>
          <li>
            <h3>写真ファイル</h3>
            <img src="@/assets/images/main/ico_madt_photo.png" alt="" class="ico"/>
            <p class="percentage">50%</p>
            <div class="range">
              <span class="gauge" style="width:50%"></span>
            </div>
          </li>
          <li>
            <h3>文書ファイル</h3>
            <img src="@/assets/images/main/ico_madt_document.png" alt="" class="ico"/>
            <p class="percentage">30%</p>
            <div class="range">
              <span class="gauge" style="width:30%"></span>
            </div>
          </li>
          <li>
            <h3>映像ファイル</h3>
            <img src="@/assets/images/main/ico_madt_video.png" alt="" class="ico"/>
            <p class="percentage">10%</p>
            <div class="range">
              <span class="gauge" style="width:10%"></span>
            </div>
          </li>
          <li class="etc">
            <h3>その他のファイル</h3>
            <img src="@/assets/images/main/ico_madt_etc.png" alt="" class="ico"/>
            <p class="percentage">10%</p>
            <div class="range">
              <span class="gauge" style="width:10%"></span>
            </div>
          </li>
        </ul>
      </div>
    </section>

  </article>
</template>

<script>
  import $ from "jquery";

  export default {


    data: function () {
      return {
        series: [2, 10, 100],
        options: {
          plotOptions: {
            radialBar: {
              dataLabels: {
                name: {
                  fontSize: '22px'
                },
                colors:{
                   
                },
                value: {
                  fontSize: '16px'
                },
                total: {
                  show: true,
                  label: '未保護',
                  formatter: function (w) {
                    // By default this function returns the average of all series. The below is just
                    // an example to show the use of custom formatter function
                    return 1
                  }
                }
              }
            }
          },
          labels: ['有効端末', '端末がオンライン', '端末がバックアップ中']
        }
      }
    },


    mounted() {
      $(document).ready(function ($) {
        jQuery("article#contents.sub .content").mCustomScrollbar({
          theme: "minimal-dark"
        });

        //셀렉트박스 UI
        jQuery(".selectbox_ui").each(function () {
          initSelectBox(jQuery(this)) //비동기로 셀렉트 박스를 만들었을 경우 initSelectBox(jQuery("#아이디")) 로 실행시켜줘야 함
        })
      });

    }


  }
</script>

<style scoped>

  section.main_backup_status .mbs_status .gauge .condition {
    position: absolute;
    top: 62px;
    left: 89px;
    width: 125px;
    height: 125px;
    text-align: center;
    padding-top: 37px;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    border-radius: 70%;
}
</style>
