/***************************************************************************
 *   Copyright (C) 2007 	Christian Schiefer, Vienna, Austria 		   *
 *  																	   *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.								   *
 *  																	   *
 *   This program is distributed in the hope that it will be useful,	   *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of 	   *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  	   *
 *   GNU General Public License for more details.   					   *
 *  																	   *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the  					   *
 *   Free Software Foundation, Inc.,									   *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.  		   *
 **************************************************************************/

// $Id: EsoParser.cpp,v 1.9 2007/02/27 21:18:22 cschiefer Exp $

#include "EsoParser.h"
#include "EsoUtil.h"
#include <QStringList>
#include <QRegExp>
#include <QtDebug>
#include <QTextStream>
#include <QFile>
#include <QFileInfo>
#include <QObject>
#include <QApplication>




EsoParser::EsoParser()
	: QObject()
{
	m_sSimulationTime = "NOT SET";
	m_sVersion = "NOT SET";
	m_iCurrentLine = 0;
	m_iVariableIndexOfTime = 2;
	m_iVariableIndexOfEnvironment = -1;
	m_iTotalLines = 0;
}

void EsoParser::Clear()
{
	m_sSimulationTime = "NOT SET";
	m_sVersion = "NOT SET";
	m_iCurrentLine = 0;
	m_iVariableIndexOfTime = 2;
	m_mapVariableInfos.clear();
	m_vEnvironments.clear();
	m_sESOFileName.clear();
	m_iVariableIndexOfEnvironment = -1;
	m_emptyVariableInfo.Clear();
	m_iTotalLines = 0;
}


EsoParser::~EsoParser()
{
}


QString EsoParser::GetESOFile() const
{
	return m_sESOFileName;
}


/* Get the EnergyPlus version. */
QString EsoParser::GetEPVersion() const
{
	return m_sVersion;
}


/* Set the EnergyPlus version. */
void EsoParser::SetEPVersion(QString const & sEPVersion)
{
	m_sVersion = sEPVersion;
}


/* Get the simulation date and time. */
QString EsoParser::GetSimulationTime() const
{
	return m_sSimulationTime;
}


/* Set the EnergyPlus version. */
void EsoParser::SetSimulationTime(QString const & sSimulationTime)
{
	m_sSimulationTime = sSimulationTime;
}


/* Get the number of simulation environments. */
int EsoParser::GetNumberOfEnvironments() const
{
	return m_vEnvironments.size();
}


/* Get the specified environment. Returns false if index is invalid. */
bool EsoParser::GetEnvironment(int iIndex, EsoEnvironment& environment) const
{
	if (iIndex >= 0 && iIndex < (int) m_vEnvironments.size())
	{
		environment = m_vEnvironments[iIndex];
		return true;
	}
	//wxLogError(_T("EsoParser::GetEnvironment: Invalid variable index %d!"),iIndex);
	return false;
}


EsoEnvironment* EsoParser::GetEnvironmentPtr(int iIndex)
{
	if (iIndex >= 0 && iIndex < (int) m_vEnvironments.size())
	{
		return &(m_vEnvironments[iIndex]);
	}
	return NULL;
}

/* Add the specified environment. */
void EsoParser::AddEnvironment(EsoEnvironment const & environment)
{
	m_vEnvironments.push_back(environment);
}

int EsoParser::GetNumLines(QFile & file, QString& sErrorMessage)
{
	//get number of lines to initialize progress bar
	//the last line looks like: "Number of Records Written=     1419392"
	QTextStream textStream(&file);
	static QRegExp eNumRecs(".*=?\\s*(\\d+)\\s*$", Qt::CaseInsensitive);

	textStream.seek(QFileInfo(file).size()- 26*sizeof(char)); //go to the end - 12 chars
	int iNumLines = 0;
	if (eNumRecs.indexIn(textStream.readLine()) != -1)
	{
		iNumLines = eNumRecs.cap(1).toInt();
	}
	textStream.seek(0);
	qDebug() << "EsoParser::GetNumLines: # lines " << iNumLines;
	return iNumLines;
}


// Parse the file.
bool EsoParser::Parse(QString const & sFileName, QString& sErrorMessage)
{
	qDebug("EsoParser::Parse(QString const & sFileName) - start");
	Clear();
	QString sLine;
	if (sFileName.isEmpty())
	{
		qDebug() << "EsoParser::Parse: Can't open file. Filename is empty!";
		sErrorMessage = tr("Can't open file '%1'!").arg(sFileName);
		return false;
	}

	//open file
	qDebug() << "EsoParser::Parse: Open file" << sFileName;
	QFile in(sFileName);
	if (!in.open(QIODevice::ReadOnly | QIODevice::Text))
	{
		qDebug() << "EsoParser::Parse: Can't open file '" << sFileName << "'!";
		sErrorMessage = tr("Can't open file '%1'!").arg(sFileName);
		return false;
	}

	m_iTotalLines = GetNumLines(in, sErrorMessage);
	QTextStream inputStream(&in);
	if (m_iTotalLines == 0)
	{
		qDebug() << "EsoParser::Parse: Number of lines is 0 " << sFileName;
		sErrorMessage = tr("File '%1' seems to be corrupt!\nCan't read final string: 'Number of Records Written'!").arg(sFileName);
		return false;
	}

	setTotalParseSteps(100);
	m_iCurrentLine = 0;
	m_sESOFileName = sFileName;
	qApp->processEvents();

	if (!ParseHeaderLine(inputStream))
	{
		qWarning() << "The file '" << m_sESOFileName << "' seems not to be an valid EnergyPlus ESO file!";
		sErrorMessage = tr("The file '%1' seems not to be an valid EnergyPlus ESO file!").arg(m_sESOFileName);
		in.close();
		return false;
	}
	//read variable names
	ParseVariableNames(inputStream);

	//read environments - read data
	ParseEnvironments(inputStream);


	//close file
	in.close();
	qDebug("EsoParser::Parse(QString const & sFileName) - end");
	return true;
}


void EsoParser::ProgressNextLine()
{
	++m_iCurrentLine;
	if (m_iCurrentLine <= 0 || m_iTotalLines <= 100)
		return;
	if (m_iCurrentLine > 0 && (m_iCurrentLine % (m_iTotalLines / 100)) == 0)
	{
		//qDebug("progress:%d", 100*m_iCurrentLine/m_iTotalLines);
		setParseProgress(100 * m_iCurrentLine / m_iTotalLines);
		qApp->processEvents();
	}
}

bool EsoParser::ParseHeaderLine(QTextStream& inputStream)
{
	qDebug() << "EsoParser::ParseHeaderLine start";
	//Program Version,EnergyPlus 1.2.1.012, 21.04.2005 00:32
	QRegExp eHeader("^Program Version\\s*,\\s*([^,]*),\\s*(.*)", Qt::CaseInsensitive);
	QString sLine;

	sLine = inputStream.readLine();
	qDebug() << "EsoParser::ParseHeaderLine total lines:" << m_iTotalLines;
	qDebug() << "EsoParser::ParseHeaderLine current line:" << m_iCurrentLine;
	ProgressNextLine();
	qDebug() << "EsoParser::ParseHeaderLine header line" << sLine;
	sLine = sLine.trimmed();
	if (eHeader.indexIn(sLine) != -1)
	{
		m_sVersion = eHeader.cap(1);
		m_sSimulationTime = eHeader.cap(2);
		qDebug() << "EsoParser::ParseHeaderLine end - OK";
		return true;
	}
	qDebug() << "EsoParser::ParseHeaderLine end - not an eso";
	return false;
}


bool EsoParser::ParseVariableNames(QTextStream& inputStream)
{
	qDebug("EsoParser::ParseVariableNames() - start");
	QString sLine;
	QString sToken;
	static QRegExp eEndVar("^End of Data Dictionary", Qt::CaseInsensitive);
	static QRegExp eEnvironment("Environment Title", Qt::CaseInsensitive);
	static QRegExp eTime("^Day of Simulation", Qt::CaseInsensitive);
	static QRegExp eUnit("([^\\[]*)\\[([^\\]]*)\\]");
	static QRegExp eComment("(!.*)");
	static QRegExp eReportStepInComment("!(Detailed|TimeStep|Hourly|Daily|Monthly|Runperiod)", Qt::CaseInsensitive);
	int iVarNumber = 0;
	QString sLine1;
	QStringList tokens;
	QStringList::iterator iter;
	QStringList::iterator iterEnd;
	//read variable names
	//until "End of Data Dictionary"
	while (!inputStream.atEnd())
	{
		sLine = inputStream.readLine();
		ProgressNextLine();
		qDebug() << "EsoParser::ParseVariableNames() - line: " << sLine;

		sLine = sLine.trimmed();
		//qDebug( "Parsing line: %s", sLine);
		if (eEndVar.indexIn(sLine) != -1)
			break;
		EsoVariableInfo varInfo;
		EvColumnInfo colInfo;
		//Split line: variable-number,number of columns, variable name [unit] !Comment or time step e.g. "!Hourly"
		//699,2,RESISTIVE ZONE,Mean Air Temperature[C] !Daily [Value,Min,Hour,Minute,Max,Hour,Minute]
		//6,2,Environment,Outdoor Dry Bulb [C] !Hourly
		//37,2,Z_E_001,Zone Transmitted Solar[W] !Hourly
		sLine1 = sLine;
		tokens = sLine1.split(",");
		iVarNumber = 0;

		if (tokens.size() < 2)
			continue;

		iter = tokens.begin();
		iterEnd = tokens.end();

		//first column: variable-number
		//ConvertFromString(iVarNumber, *iter, std::dec);
		if (iter == iterEnd)
			continue;
		iVarNumber = (*iter).toInt();
		qDebug("EsoParser::Variable number: %d", iVarNumber);
		varInfo.SetIndex(iVarNumber);

		//second column: number of columns
		++iter;
		if (iter == iterEnd)
			continue;
		int iNumCols = 0;
		iNumCols = (*iter).toInt();

		qDebug("EsoParser::Column number: %d", iNumCols);

		QString sComment;
		QString sReportStep;
		int i = 0;
		//other colums:
		//while ( tkz.HasMoreTokens() )
		++iter;
		for (; iter != iterEnd; ++iter)
		{
			//  	  qDebug( "EsoParser:: Col: %s", (*iter). );
			sToken = *iter;
			if (eEnvironment.indexIn(sToken) != -1)
				m_iVariableIndexOfEnvironment = iVarNumber;
			if (eTime.indexIn(sToken) != -1)
				m_iVariableIndexOfTime = iVarNumber;
			//extract comment
			int iPos = eComment.indexIn(sToken);
			if (iPos != -1)
			{
				colInfo.m_sName = sToken.mid(0, iPos);
				sComment = eComment.cap(1);
				// Parse report step
				if (eReportStepInComment.indexIn(sComment) != -1)
				{
					sReportStep = eReportStepInComment.cap(1);
					varInfo.SetReportStep(ToReportStep(sReportStep));
					sComment = sToken.mid(sComment.size() + sReportStep.size());
				}
				varInfo.SetComment(sComment);
			} else
				colInfo.m_sName = sToken;

			//extract unit [...]
			if (eUnit.indexIn(colInfo.m_sName) != -1)
			{
				colInfo.m_sName = eUnit.cap(1);
				colInfo.m_sUnit = eUnit.cap(2);
			}
			else
			{
                colInfo.m_sUnit =  "-";
			}

			++i;
			//add colInfo to varInfo
			varInfo.AddColumnInfo(colInfo);
			colInfo.Clear();
			qDebug("EsoParser::ParseVariableNames() - %d", i);
		}
		if (i != iNumCols)
		{
			//  		  wxLogError( wxT("Invalid number of colums for Variable: %s\nExpected %d, got %d" ),"",iNumCols,i);
		}
		//add varInfo to map
		m_mapVariableInfos.insert(std::make_pair(iVarNumber, varInfo));
	}

	qDebug("EsoParser::ParseVariableNames() - end");
	return true;
}


bool EsoParser::ParseEnvironments(QTextStream& inputStream)
{
	qDebug("EsoParser::ParseEnvironments() - start");
	static QRegExp eEndOfData("End of Data", Qt::CaseInsensitive);
	EsoEnvironment* pEnvironment = NULL;

	QString sToken;
	int iVarNumber = 0;
	float fVal;
	QString sLine;
	EsoVariableInfo infoTime = GetVariableInfo(m_iVariableIndexOfTime);
	//2,8,Day of Simulation[],Month[],Day of Month[],DST Indicator[1=yes 0=no],Hour[],StartMinute[],EndMinute[],DayType
	int iDayOfSimCol = 1; //starting with 0
	int iMonthCol = 2;
	int iDayOfMonthCol = 3;
	int iDSTCol = 4;
	int iHourCol = 5;
	int iStartMinCol = 6;
	int iEndMinCol = 7;
	int iDayTypeCol = 8;
	bool bAddDetailed = false;
	bool bAddTimeStep = false;
	bool bAddHourly = false;
	bool bAddDaily = false;
	bool bAddMonthly = false;
	bool bAddRunperiod = false;
	EvTimeStruct time;

	std::vector<int> vVariableIdsDetailed;
	std::vector<int> vVariableIdsTimeStep;
	std::vector<int> vVariableIdsHourly;
	std::vector<int> vVariableIdsDaily;
	std::vector<int> vVariableIdsMonthly;
	std::vector<int> vVariableIdsRunperiod;
	GetVariableIds(EvDetailed, vVariableIdsDetailed);
	GetVariableIds(EvTimeStep, vVariableIdsTimeStep);
	GetVariableIds(EvHourly, vVariableIdsHourly);
	GetVariableIds(EvDaily, vVariableIdsDaily);
	GetVariableIds(EvMonthly, vVariableIdsMonthly);
	GetVariableIds(EvRunPeriod, vVariableIdsRunperiod);

	while (!inputStream.atEnd())
	{
		sLine = inputStream.readLine();
		ProgressNextLine();
		sLine = sLine.trimmed();

		//end of data
		if (eEndOfData.indexIn(sLine) != -1)
		{
			if (pEnvironment != NULL)
			{
				AddEnvironment(*pEnvironment);
			}
			pEnvironment = NULL;
			break;
		}

		QString sLine1 = sLine;
		QStringList tokens = sLine1.split(",");
		//first column: variable-number
		if (tokens.size() < 2)
		{
			continue;
		}

		iVarNumber = tokens.first().toInt();

		//check for new environment
		//1,TAMPA FL USA TMY2-12842 WMO#=722110,  27.97, -82.53,  -5.00,   3.00
		if (iVarNumber == m_iVariableIndexOfEnvironment)
		{
			if (pEnvironment != NULL)
			{
				AddEnvironment(*pEnvironment);
			}
			qDebug("New environment starts!");
			pEnvironment = new EsoEnvironment;
			EsoVariableInfo info = GetVariableInfo(m_iVariableIndexOfEnvironment);

			int i = 0;
			QStringList::iterator iter;
			QStringList::iterator iterEnd(tokens.end());
			QVector< EvEnvInfoVar> vEnvInfo;
			for (iter = ++tokens.begin(); iter != iterEnd; ++iter, ++i)
			{
				EvEnvInfoVar envVar;
				envVar.sTitle = info.GetColumnInfo(i).m_sName;
				envVar.sUnit = info.GetColumnInfo(i).m_sUnit;
				envVar.sValue = *iter;
				vEnvInfo.push_back(envVar);
			}
			pEnvironment->SetInfo(vEnvInfo);
			qDebug() << "Environment info: " << pEnvironment->GetInfo(false);
		}
		//new time step
		else if (iVarNumber == m_iVariableIndexOfTime)
		{
			bAddDetailed = true;
			bAddTimeStep = true;
			bAddHourly = true;
			bAddDaily = true;
			bAddMonthly = true;
			bAddRunperiod = true;
			int i = 0;
			QStringList::iterator iter;
			QStringList::iterator iterEnd(tokens.end());
			for (iter = tokens.begin(); iter != iterEnd; ++iter, ++i)
			{
				if (i == iDayOfSimCol)
					time.iDayofSimulation = (*iter).toInt();
				else if (i == iMonthCol)
					time.iMonth = (*iter).toInt();
				else if (i == iDayOfMonthCol)
					time.iDayOfMonth = (*iter).toInt();
				else if (i == iDSTCol)
					time.bDST_Indicator = ((*iter).toInt() == 1) ? true : false;
				else if (i == iHourCol)
					time.iHour = (*iter).toInt() -1; //we store the hour starting from 0 not 1
				else if (i == iStartMinCol)
					time.iStartMinute = (int) (*iter).toFloat();
				else if (i == iEndMinCol)
					time.iEndMinute = (int) (*iter).toFloat();
				else if (i == iDayTypeCol)
					time.iDayType = ToDayType((*iter));
			}
		} else
		{
		  	//only the following elements have more than 2 colums:
		  	//1,5,Environment Title[],... (already handled)
		  	//2,6,Day of Simulation[],...
		  	//3,3,Cumulative Day of Simulation[],...
		  	//4,2,Cumulative Days of Simulation[],...
		  	//and some other varialbes store additional info about max/min values e.g.:
		  	//699,2,RESISTIVE ZONE,Mean Air Temperature[C] !Daily [Value,Min,Hour,Minute,Max,Hour,Minute]
		  	//TODO: support additional infos.

			EsoVariableInfo info = GetVariableInfo(iVarNumber);
			EvReportStep varStep = info.GetReportStep();

			if (varStep == EvDetailed && bAddDetailed)
			{
				pEnvironment->AddTime(EvDetailed, time);
				bAddDetailed = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsDetailed.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsDetailed[i]);
				}
			} else if (varStep == EvTimeStep && bAddTimeStep)
			{
				pEnvironment->AddTime(EvTimeStep, time);
				bAddTimeStep = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsTimeStep.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsTimeStep[i]);
				}
			} else if (varStep == EvHourly && bAddHourly)
			{
				pEnvironment->AddTime(EvHourly, time);
				bAddHourly = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsHourly.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsHourly[i]);
				}
			} else if (varStep == EvDaily && bAddDaily)
			{
				pEnvironment->AddTime(EvDaily, time);
				bAddDaily = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsDaily.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsDaily[i]);
				}
			} else if (varStep == EvMonthly && bAddMonthly)
			{
				pEnvironment->AddTime(EvMonthly, time);
				bAddMonthly = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsMonthly.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsMonthly[i]);
				}
			} else if (varStep == EvRunPeriod && bAddRunperiod)
			{
				pEnvironment->AddTime(EvRunPeriod, time);
				bAddRunperiod = false;
				//initialize all variables with NAN
				for (unsigned i=0; i<vVariableIdsRunperiod.size(); ++i)
				{
				  	pEnvironment->AddDataInit(vVariableIdsRunperiod[i]);
				}
			}
			
		  	fVal = (*++tokens.begin()).toDouble();
		  	pEnvironment->AddData(iVarNumber, fVal);
		}
	}
	if (pEnvironment != NULL)
	{
		AddEnvironment(*pEnvironment);
		qWarning("No 'End of Data' found! This file seems to be corrupt!");
		return false;
	}
	qDebug("EsoParser::ParseEnvironments() - end");
	return true;
}


void EsoParser::GetVariableIds(EvReportStep reportStep, std::vector<int> & vVariableIds)
{
	qDebug() << "EsoParser::GetVariableIds " << reportStep;
    vVariableIds.clear();
	std::map< int,EsoVariableInfo>::iterator iter;
	std::map< int,EsoVariableInfo>::iterator iterEnd(m_mapVariableInfos.end());
	for (iter = m_mapVariableInfos.begin(); iter!=m_mapVariableInfos.end(); ++iter)
	{
		if (iter->second.GetReportStep() == reportStep )
		{
			vVariableIds.push_back(iter->first);
		}
	}
	qDebug() << "EsoParser::GetVariableIds found " << vVariableIds.size() << "for report step "<< reportStep;
}


EsoVariableInfo EsoParser::GetVariableInfo(int iIndex) const
{
	std::map< int,EsoVariableInfo>::const_iterator iterInfo(m_mapVariableInfos.find(iIndex));
	if (iterInfo == m_mapVariableInfos.end())
	{
		//wxLogError( "No such variable with id %d",iIndex );
		return m_emptyVariableInfo;
	}
	return iterInfo->second;
}


void EsoParser::GetVariableInfo(std::map< int,EsoVariableInfo>::const_iterator& iterBegin, std::map< int,EsoVariableInfo>::const_iterator& iterEnd)
{
	iterBegin = m_mapVariableInfos.begin();
	iterEnd = m_mapVariableInfos.end();
	while (iterBegin->first < 6 && iterBegin != iterEnd) //ignore environment definition variables
	{
		++iterBegin;
	}
	iterEnd = m_mapVariableInfos.end();
}


QString EsoParser::GetVariableTitle(int iVar)
{
	EsoVariableInfo info = GetVariableInfo(iVar);
	return (info.GetColumnInfo(1).m_sName + " " + info.GetColumnInfo(0).m_sName);
}
