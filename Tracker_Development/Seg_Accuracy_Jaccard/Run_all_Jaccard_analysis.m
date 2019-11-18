clear
%Specify: folder, file pattern (model to be used), ModelType and Channel 
%Check table written out does not overwrite previously names table!!
%calls 'calculatejaccard.m'
%All files need to be in the format 'mask_posX_X', and all models
%'[Model]_posX_X'. For example 'mask_pos2_2' and 's_pos2_2' for scribble
%model

 ModelType = 1 %specify scrib model (1) Ras model v1 (2) Ras model v2 (3) etc


% Specify the folder where the files live.
myFolder = 'C:\Users\Jasmine\Desktop\PHDnew\Segmentation accuracy\Segmented\Jaccardcode_andfiles';
% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(myFolder)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', myFolder);
  uiwait(warndlg(errorMessage));
  return;
end
% Get a list of all files in the folder with the desired file name pattern.
filePatternmask = fullfile(myFolder, 'mask_*.tif'); % Change to whatever pattern you need.
theFilesmask = dir(filePatternmask);

filePatternseg = fullfile(myFolder, 's_*.tif'); % Change to whatever pattern you need.
theFilesseg = dir(filePatternseg);

%create an empty table
StatsTable = array2table(zeros(0,9), 'VariableNames',{'ModelType', 'Channel', 'MaskObjectNo', 'SegObjectNo', 'TP','FP','FN','DoubleSeg','JaccardObjects'});    
    
for k = 1:length(theFilesmask) %specify file couple (mask and segmented)
      
  baseFileNamemask = theFilesmask(k).name;
  baseFileNameseg = theFilesseg(k).name;
  fullFileNamemask = fullfile(myFolder, baseFileNamemask);
  fullFileNameseg = fullfile(myFolder, baseFileNameseg);
  fprintf(1, 'Now reading %s\n', baseFileNamemask);
  fprintf(1, 'Now reading %s\n', baseFileNameseg);
  %run the jaccard calculations
  for Channel=1:2
     clearvars -except Channel baseFileNamemask baseFileNameseg fullFileNamemask fullFileNameseg StatsTable ModelType myFolder filePatternmask filePatternSeg theFilesmask theFilesseg k  
  calculatejaccard
  %Save to table
  StatsTableValues = table(ModelType, Channel, MaskObjectNo, SegObjectNo, TP, FP, FN, DoubleSeg, JaccardObjects)
  StatsTable = [StatsTable; StatsTableValues]
  end
end

writetable(StatsTable, 'JaccardStatsTable_Scribblemodel.dat')
writetable(StatsTable, 'JaccardStatsTable_Scribblemodel.txt')