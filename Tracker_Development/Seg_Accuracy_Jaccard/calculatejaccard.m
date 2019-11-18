
segmented1 = imread(fullFileNameseg); %load segmented file
ind = true(size(segmented1));
%all ones get replaced with zeros so only RFP segmentation (inx=2) is left (all 
%twos if want GFP i.e change inx=1)
for idx = Channel
    ind = ind & segmented1 ~= idx;
end
segmented1(ind) = 0;


ind = true(size(segmented1));
%all twos get replaced with ones so Jaccard index can be calculated 
for idx = 0
    ind = ind & segmented1 ~= idx;
end
segmented1(ind) = 1;


mask1 = imread(fullFileNamemask, Channel); %load RFP channel of hand drawn (2)
%load GFO channel of hand drawn (1)

ind = true(size(mask1));
%all numbers not 0 get replaced with 1s in hand drawn mask for Jaccard  
for idx = 0
    ind = ind & mask1 ~= idx;
end
mask1(ind) = 1;

%convert to logical image
logicalseg = segmented1 ~= 0;
logicalmask = mask1 ~= 0;


while (~any(logicalmask) ~=0)
   MaskObjectNo=0
   SegObjectNo=0
   TP=0
   FP=0
   FN=0
   DoubleSeg=0
   JaccardObjects=0     
return 
end

%Jaccard calculations 
[jaccardInx, jaccardDist] = jaccard_coefficient(logicalmask, logicalseg);

%calculate number of objects
maskobjects = bwconncomp(logicalmask);
MaskObjectNo = maskobjects.NumObjects;


segobjects = bwconncomp(logicalseg);
SegObjectNo = segobjects.NumObjects;

%number of segmented objects/number of objects in mask
segobjects.NumObjects/maskobjects.NumObjects;

%calculate centroids of SEGMENTATION and object circle and display on overlay of image

statsseg = regionprops('table',logicalseg,'Centroid',...
    'MajorAxisLength','MinorAxisLength');
centersseg = statsseg.Centroid;
diametersseg = mean([statsseg.MajorAxisLength statsseg.MinorAxisLength],2);
radiiseg = diametersseg/2;
statsseg.Radii = radiiseg;

%discarding objects too small to be cells
% Sdseg = std(radiiseg)
% Mnseg = mean(radiiseg)
% LQseg = Mnseg-Sdseg
% 
% thresholdminseg = LQseg;
% statsseg(statsseg.Radii < thresholdminseg, :) = []
% radiinewseg = statsseg.Radii;
% centersnewseg = statsseg.Centroid;

%calculate centroids of MASK and object circle and display on overlay of image

statsmask = regionprops('table',logicalmask,'Centroid',...
    'MajorAxisLength','MinorAxisLength');
centersmask = statsmask.Centroid;
diametersmask = mean([statsmask.MajorAxisLength statsmask.MinorAxisLength],2);
radiimask = diametersmask/2;
statsmask.Radii = radiimask;

%discarding objects too small to be cells
% Sdmask = std(radiimask)
% Mnmask = mean(radiimask)
% LQmask = Mnmask-Sdmask
% 
% thresholdminmask = LQ;
% statsmask(statsmask.Radii < thresholdminmask, :) = []
% radiinewmask = statsmask.Radii;
% centersnewmask = statsmask.Centroid;


centroidsseg = cat(1, statsseg.Centroid);
% imshow(logicalseg)
% hold on
% plot(centersnewseg(:,1), centersnewseg(:,2), 'b*')
% hold on
hold on
imshow(logicalmask)
hold on
plot(centersmask(:,1), centersmask(:,2), 'b*')
hold on
viscircles(centersmask,radiimask);
hold on
viscircles(centersseg,radiiseg, 'Color', 'b');
hold off

%detecting similar objects

for i=1:length(centersmask)
MatchMaskC = centersmask(i,:);
mmax = centersmask(i,:)+radiimask(i);
mmin = centersmask(i,:)-radiimask(i);
MatchSegC = centersseg(centersseg(:,1) > mmin(:,1) & centersseg(:,1) < mmax(:,1) & centersseg(:,2) > mmin(:,2) & centersseg(:,2) < mmax(:,2), :);

MatchStatsMS(i,:) = table({MatchMaskC},{MatchSegC},...
    'VariableNames',{'Mask' 'Seg'});

end 

for i=1:length(centersseg)
MatchSegCen = centersseg(i,:);
mmax = centersseg(i,:)+radiiseg(i);
mmin = centersseg(i,:)-radiiseg(i);
MatchMaskCen = centersmask(centersmask(:,1) > mmin(:,1) & centersmask(:,1) < mmax(:,1) & centersmask(:,2) > mmin(:,2) & centersmask(:,2) < mmax(:,2), :);

MatchStatsSM(i,:) = table({MatchSegCen},{MatchMaskCen},...
    'VariableNames',{'Seg' 'Mask'});

end 

%calculate the mappings of the overlapping objects and add a coloumn to the
%tables- 0 if no overlap, 1 if exact overlap, 2 or more if more than one
%cell is segmented for one true object
for i=1:numel(MatchStatsMS.Seg)
MatchStatsMS.Count{i} = size(MatchStatsMS.Seg{i},1);
end

for i=1:numel(MatchStatsSM.Mask)
MatchStatsSM.Count{i} = size(MatchStatsSM.Mask{i},1);
end

%for any objects counted as '2' in seg-mask, change those values for the
%mask coordinates in mask-seg to 0 (so not to count incorrectly double
%segmented objects as TP or to avoid double counting FP
%Also count these objects as a variable DoubleSeg
DoubleSeg = 0;
for i=1:numel(MatchStatsSM.Mask)
    if MatchStatsSM.Count{i} == 2;
        DoubleSeg=DoubleSeg+1;
       MatchStatsSM.Coords{i} = MatchStatsSM.Mask{i}(1,1);
       MatchStatsSM.Coords2{i} = MatchStatsSM.Mask{i}(2,1);
    else if MatchStatsSM.Count{i} == 1;
        MatchStatsSM.Coords{i} = 0;   
        MatchStatsSM.Coords2{i} = 0;
        end
    end 
end

for i=1:numel(MatchStatsMS.Mask);
    A = MatchStatsMS.Mask{i}(1,1);
for j = 1:numel(MatchStatsSM.Coords);
    if A == MatchStatsSM.Coords{j};
    MatchStatsMS.Count{i} = 0;
    end
end
for k = 1:numel(MatchStatsSM.Coords2)
    if A == MatchStatsSM.Coords2{k};
    MatchStatsMS.Count{i} = 0;
    end
end
end

%calculating number of TP (Mask maps to Segmented MS count = 1), 
%FP (Segmented but no mask SM count=0) and
%FN (SM count is 0-did not segment, or >1 segmented one object as more than one) 
%and calculating the Jaccard index for objects 

    TP = 0;
    FP = 0;
    FN = 0;
for i=1:numel(MatchStatsMS.Count)
    if MatchStatsMS.Count{i} == 1; 
        TP=TP+1;
        else if MatchStatsMS.Count{i} == 0;
                FN=FN+1;
            else if MatchStatsMS.Count{i} > 1
                    FN=FN+1;
                end
            end
    end
end

 for i=1:numel(MatchStatsSM.Count)
     if MatchStatsSM.Count{i} == 0;
            FP=FP+1;
     end
 end

 %Fraction of two cells segmented as one
 FractionDouble= (DoubleSeg*2)/numel(MatchStatsMS.Mask)
 %Jaccard index calculations  TP/TP+FP+FN
 JaccardObjects= TP/(TP+FP+FN)