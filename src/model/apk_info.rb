class ApkInfo
  attr_accessor :package_name
  attr_accessor :version_code
  attr_accessor :version_name
  attr_accessor :app_name
  attr_accessor :ic_launcher
  attr_accessor :metas

  def initialize(apk_path)
    load_infos(`aapt d badging #{apk_path}`.split("\n"))

    load_metas(`aapt dump xmltree #{apk_path} AndroidManifest.xml`.split("\n"))
  end

  def to_string
    puts <<-EOB
appName\t#{self.app_name}
icLauncher\t#{self.ic_launcher}
packageName\t#{self.package_name}
versionCode\t#{self.version_code}
versionName\t#{self.version_name}
#{self.metas.inject([]){|acc,(k,v)| acc<<"meta:#{k}\t#{v}";acc}.join("\n")}
    EOB
  end

  private

  def load_infos(infos)
    infos.each do |info|
      key_dict = analyze_key_value(info)
      if info.include?('package') && info.include?('versionCode=')
        self.package_name = key_dict['name']
        self.version_code = key_dict['versionCode']
        self.version_name = key_dict['versionName']
        next
      end

      if info.include?('application') && info.include?('label=') && info.include?('icon=')
        self.app_name= key_dict['label']
        self.ic_launcher = key_dict['icon']
      end
    end
  end

  # 获取应用meta信息
  def load_metas(xml_tree)
    self.metas = {}
    xml_tree.each_with_index { |info, i|
      if info.include?('E: meta-data')
        name = xml_tree[i + 1].gsub("\n", '').split("=\"")[1].split("\"")[0]
        if xml_tree[i + 2].include?('type 0x')
          value = xml_tree[i + 2].gsub('\n', '').split('type 0x')[1].split(')')[1]
        elsif xml_tree[i + 2].include?('android:resource')
          value = xml_tree[i + 2].gsub("\n", '').split(')=')[1]
        elsif xml_tree[i + 2].include?('=@0x')
          value = "@" + xml_tree[i + 2].gsub("\n", '').split("=@")[1]
        else
          value = xml_tree[i + 2].gsub("\n", '').split("=\"")[1].split("\"")[0]
        end
        self.metas[name] = value
      end

    }
  end

  def analyze_key_value(xml_str='')
    key_dict = {}
    xml_str.split(" ").each do |package_item|
      item_array = package_item.split("=")
      if item_array.size != 2
        next
      end
      key_dict[item_array[0]] = item_array[1].gsub("'", '').gsub("\n", '')
    end
    key_dict
  end
end