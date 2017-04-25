# coding: utf-8
class MergeApk

  attr_accessor :src_file_path
  attr_accessor :target_file_path

  attr_accessor :src_public_ids # 类似地：{'<app_name«string>': '0x7f030000','<mi_ic_launcher«drawable>':'0x7f020001'}
  attr_accessor :target_public_ids
  attr_accessor :merged_public_ids

  attr_accessor :new_package

  def initialize(src_apk_path, target_apk_path, new_package)
    self.new_package = new_package
    ChangeApk.new(src_apk_path, self.new_package).start
    ChangeApk.new(target_apk_path, self.new_package).start
    self.src_file_path = src_apk_path.gsub(".apk", '')
    self.target_file_path = target_apk_path.gsub(".apk", '')
    self.src_public_ids = {}
    self.target_public_ids = {}
    self.merged_public_ids = {}
  end

  def start
    puts "start to merge files"

    init_public_ids("#{self.src_file_path}/res/values/public.xml", :src_public_ids)
    init_public_ids("#{self.target_file_path}/res/values/public.xml", :target_public_ids)

    self.smali_0x_ids_replace(self.src_file_path, self.src_public_ids)
    self.smali_0x_ids_replace(self.target_file_path, self.target_public_ids)

    #移动特别的代码库，防止代码冲突
    #FIXME::
    move_package = MovePackage.new(self.target_file_path)
    move_package.start('com.umeng.analytics', 'extra.merge.umeng.analytics')
    move_package.start('okhttp3', 'extra.merge.ko3http')
    move_package.start('android.support', 'extra.merge.support.android')
    move_package.start('com.nostra13.universalimageloader', 'extra.merge.nostra13.universalimageloader')
    move_package.start('u.aly', 'extra.merge.aly.yo')

    self.merge_files(self.src_file_path)

    init_public_ids("#{self.target_file_path}/res/values/public.xml", :merged_public_ids)
    puts self.merged_public_ids
    self.smali_0x_ids_recover(self.target_file_path, self.merged_public_ids)
  end

  #将public.xml中的id读取到内存
  def init_public_ids(xml_path, hash_attr=:src_public_ids)
    target_doc = REXML::Document.new(File.new(xml_path))
    target_root = target_doc.root
    target_root.get_elements('public').each do |node|
      type = node.attributes['type'].to_s.to_sym
      name = node.attributes['name'].to_s
      id = node.attributes['id'].to_s
      self.send(hash_attr)["<#{name}«#{type}>"]=id
    end
  end

  # #将smali中包含 0x7f..... 的字符串重新命名（根据public.xml来命名）
  def smali_0x_ids_replace(unziped_path, ids={})
    Dir::entries(unziped_path).each do |filename|
      child_path = "#{unziped_path}/#{filename}"
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(child_path)
        smali_0x_ids_replace(child_path, ids)
        next
      end
      if filename.end_with?("smali")

        if child_path.include?("/android/support/")
          next
        end

        contents = []
        File.readlines(child_path).each do |line|

          gsubed_line = line
          line.scan(/(0x7f[\d|a-f]{6})/) do |matched| #FIXME::应该忽略这些变量 0x7f000000000000L
            next if matched.empty?
            key = ids.key(matched[0])
            next unless key
            gsubed_line = gsubed_line.gsub(matched[0], key) #'<app_name«string>'
            puts "#{child_path}:#{matched[0]}\t#{key}"
          end
          contents << gsubed_line
        end

        File.open(child_path, "w+") do |f|
          f.puts contents.join("")
          f.close
        end
      end
    end
  end

  # #将smali中包含 <app_name«string> 重新定义为 0x7f.....
  def smali_0x_ids_recover(unziped_path, ids={})
    Dir::entries(unziped_path).each do |filename|
      child_path = "#{unziped_path}/#{filename}"
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(child_path)
        smali_0x_ids_recover(child_path, ids)
        next
      end
      if filename.end_with?("smali")

        if child_path.include?("/android/support/")
          next
        end

        contents = []
        File.readlines(child_path).each do |line|

          gsubed_line = line
          line.scan(/(<[\S!«]+«[\S!«]+>)/) do |matched|
            id = ids[matched[0]]
            next unless id
            gsubed_line = gsubed_line.gsub(matched[0], id) #'<app_name«string>'
            gsubed_line = gsubed_line.gsub('const/high16', 'const')
            puts "#{child_path}:#{matched[0]}\t#{id}"
          end
          contents << gsubed_line
        end

        File.open(child_path, "w+") do |f|
          f.puts contents.join("")
          f.close
        end
      end
    end
  end

  def merge_files(src_path)
    Dir::entries(src_path).each do |filename|
      src_child_path = "#{src_path}/#{filename}"
      target_child_path = "#{src_child_path.gsub(Regexp.new("^#{self.src_file_path}"), self.target_file_path)}"
      if filename=='.' || filename=='..'
        next
      end
      if File.directory?(src_child_path)
        system("[ ! -d #{target_child_path.gsub("$", "\\$")} ] && mkdir #{target_child_path.gsub("$", "\\$")}")
        merge_files(src_child_path)
        next
      end

      #如果目标apk包含友盟等信息,忽略友盟等信息的合并
      # if
      #     src_child_path.include?("smali/com/tencent/mm") ||
      #     src_child_path.include?("smali/android/support") ||
      #     src_child_path.include?("unknown/com/tencent/mm")
      #   next
      # end
      # if src_child_path.include?("smali/okhttp3")
      #   next
      # end
      # if src_child_path.include?("smali/com/umeng")
      #   next
      # end

      if !File.exists?(target_child_path)
        # puts "cp #{src_child_path.gsub("$", "\\$")} #{target_child_path.gsub("$", "\\$")}"
        system("cp #{src_child_path.gsub("$", "\\$")} #{target_child_path.gsub("$", "\\$")}")
      elsif src_child_path.include?('original/')
      elsif filename.end_with? '.xml'
        # puts "merge xml\t#{src_child_path} #{target_child_path}"
        MergeXml.new(src_child_path, target_child_path)
      elsif File.exists?(target_child_path)
        next
      else
      end
    end
  end
end