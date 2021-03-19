function pull(c_Name, c_Realm) {
  
      if (!c_Name || c_Name == 'Unknown')
      {
        return "Invalid Name"
      }
        if(!c_Realm)
      {
        return "Invalid Realm"
      }
      
      var apikey = "USzClAwPh59lFwNDkbT6A9oBgcKjnvWxMG"
      var utfoffset = '-8'
      var timestring = "Server Time"
      var region = "us"

      var c_JSON = UrlFetchApp.fetch("https://"+region+".api.blizzard.com/profile/wow/character/"+c_Realm+"/"+c_Name+"?namespace=profile-us&locale=en_US&access_token="+apikey+"",{muteHttpExceptions:true})
      if (c_JSON.getResponseCode() == 404) {
        return "Not Found"
      }
      var c = JSON.parse(c_JSON);
      var job = 0;
      if(c.character_class.id == "1")  { job = "Warrior"; }
      else if(c.character_class.id == "2")  { job = "Paladin"; }
      else if(c.character_class.id == "3")  { job = "Hunter"; }
      else if(c.character_class.id == "4")  { job = "Rogue"; }
      else if(c.character_class.id == "5")  { job = "Priest"; }
      else if(c.character_class.id == "6")  { job = "Death Knight";}
      else if(c.character_class.id == "7")  { job = "Shaman";}
      else if(c.character_class.id == "8")  { job = "Mage";}
      else if(c.character_class.id == "9")  { job = "Warlock";}
      else if(c.character_class.id == "10")  { job = "Monk"}
      else if(c.character_class.id == "11")  { job = "Druid" }
      else if(c.character_class.id == '12') { job = "Demon Hunt"}
      else  {job == "N/A"}

      var c_Data = new Array(
        job
      
      )

      var c_Array = new Array(c_Data); return c_Array
    }
