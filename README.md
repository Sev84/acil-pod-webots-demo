# ACIL-POD | Webots R2025a online demo

Bu paket bir eğitim simülasyonudur; fiziksel aracın, ESP32 devresinin, telefon bağlantısının veya gerçek bir acil durum uygulamasının çalıştığının kanıtı değildir. Öğrenci adı, takım adı, okul bilgisi ve özel test görüntüleri içermez. Ayrı bir telefon sunucusu veya üçüncü taraf ölçüm hizmeti eklenmemiştir.

## Webots'ta yerel çalıştırma

1. Webots R2025a ile **worlds/acil_pod.wbt** dosyasını açın ve gerçek zamanlı oynatın.
2. **Robot Window** / **ACIL-POD** kumandasını açın. Yön düğmesini basılı tutarak sürün; bırakır bırakmaz dur komutu gider. Pencere kapanırsa, bağlantı kesilirse veya simülasyon duraklarsa komutlar yenilenmez; hareket süresi sınırı aracı durdurur.
3. Engel eşiğine (0,20 m) yaklaşan araç durur. Araç durduktan sonra yanlış kodu deneyin; kapak kapalı kalır. Sonra demo kodu **1234** ile kapağı açın. Kapak açıkken sürüş kilitli kalır. Kapağı kapatın; engel yakınsa sadece kapatmak hareketi yeniden açmaz. Gerekirse gösterimi sıfırlayın.
4. Masaüstü yedeği: sahne odaktayken **W/A/S/D**, **X** dur, **1234 + Enter** (veya P), **C** kapağı kapat. Tarayıcıda önerilen kontrol paneldeki düğmelerdir, sahne klavyesi değil.

Yerel komut:

    webots --mode=realtime --stdout --stderr worlds/acil_pod.wbt

## Webots.cloud dağıtım taslağı: henüz canlı değil

Kullanıcının ayrıca yetkilendirdiği bir GitHub deposuna **yalnız bu klasörün içeriği** gönderilirse Cyberbotics'in dokümantasyonundaki **Add a new simulation** ekranında GitHub dünya sayfasının URL'si (sürüm dalı veya etiket + worlds/acil_pod.wbt) kullanılabilir. Dockerfile, Webots.cloud R2025a Ubuntu 22.04 taban etiketini kullanır. webots.yml ve aynı içerikli webots.yaml dosyaları **publish: false** ile hazırlanmıştır.

**Listelenmeme gizlilik değildir**: depo veya çalışan bağlantı erişim kontrolü değildir. R2025a kılavuzu liste dışı derken servis deposu senkronizasyonda yüklenmemeyi söylüyor. Bu ayarla bağlantının çalışacağı garanti edilmez. Başarılı dağıtım ve bağlantı doğrulanmadan jüriye çalışan bir çevrimiçi adres verilmemelidir. Ayarı otomatik olarak true yapmayın ve depoyu otomatik olarak açık yapmayın.

## Teknik kontrol

* Ön sensör 0–2 m; 2 m yakın isabet görülmediği anlamına gelebilir. Kapak açısı Webots konum sensöründen gelir. Düğmeler, resmî R2025a RobotWindow.js ve WWI üzerinden yalnız sabit simülasyon komutları gönderir.
* Paket ve JavaScript/Python sözdizimi yerelde kontrol edilmiştir. Webots.cloud sunucusuna gönderme, sunucu Docker derlemesi, tarayıcı → WWI canlı uçtan uca akışı, paylaşım bağlantısı, mobil bağlantı ve erişim bu hazırlıkta doğrulanmış değildir.

Resmî kaynaklar:

- https://github.com/cyberbotics/webots/blob/R2025a/docs/guide/webots-cloud.md
- https://github.com/cyberbotics/webots-cloud-simulation-template
- https://github.com/cyberbotics/webots/tree/R2025a/projects/samples/howto/custom_robot_window_simple
